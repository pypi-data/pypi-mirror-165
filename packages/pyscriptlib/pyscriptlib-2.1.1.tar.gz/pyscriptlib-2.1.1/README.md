## Pyscriptlib - Python Bash Script Helpers

***pyscriptlib*** is a collection of helper functions that make it easy to invoke `bash` shell commands from a python script.

These helpers simplify the use of the `sys`, `os`, and `subprocess` modules for common cases.

From `sys` we get:
- `arg(n:int) -> str`
  - a simple parse of `sys.argv` that always returns a string
  - also consider `argparse` or `click-shell` if you are building a complex CLI
- `nargs(n:int) -> List(str)`
  - retrieve the remaining command line args starting with `arg(n)`
- `shift(n:int=1) -> List[str]`
  - shifts `sys.argv` by `n` preserving `sys.argv[0]` returning removed args
- `exit(return_code:int=0)`
  - exeunt, pursued by a bear (WS)

From `os` we get:
- `env(var:str) -> str|None`
  - easy retrieval of environment variables
- `kill(pid:int, signal:int=9)`
  - this subprocess is killing me, so kill or be killed

From `subprocess` we get several useful variations of `sh*(cmd:str, **kwargs)` to invoke the `/bin/bash` shell for us (including `subprocess.Popen(**kwargs)` if necessary):
- `sh(cmd:str, **kwargs)  -> (stdout+stderr).strip()`
  - output, output, gimme output
- `shl(cmd:str, **kwargs) -> list(rc, stdout, stderr)`
  - ok, ok, maybe we should take a look first: `if rc == 0`
- `shk(cmd:str, **kwargs) -> list(is_ok, rc, stdout, stderr)`
  - let's test with a concise boolean `is_ok` instead of `rc == 0`
- `sho(cmd:str, **kwargs) -> CompletedProcess(is_ok, rc, stdout, stderr)`
  - `cp = sho(cmd)` is the full Monty
  - customized with `cp.is_ok` and `cp.rc` 
- `shx(cmd:str, **kwargs) -> None`
  - displays live output to terminal just like you want it to in living color
- `shb(cmd:str, **kwargs) -> int(pid)`
  - runs `cmd` in background, returning immediately
  - use `pid` to `kill(pid)`, or not, you daemon you 

And, from nowhere in particular, we get
- `humanize(seconds:int, style='compact', days='days', zerodays=True) -> str()`
  - returns a human readable form of elapsed seconds such as `/proc/uptime`
  - full `'05 days 03:59:27'` or compact `'05d 03h 59m 27s'`

### Installation
***pyscriptlib*** is available at ***pypi.org***
```bash
pip install pyscriptlib
```

### Example Usage
See ***pyscriptlib/example_script.py*** below
```python
#! /usr/bin/env python3
'''
Usage: python3 /path/to/site-packages/pyscriptlib/example_script.py ~/some/example/dir arg2 arg3
'''

from pathlib import Path
import time
from pyscriptlib import arg, nargs, shift, env, sh, shx, shl, shk, sho, shb, kill, humanize

def title(descr, code):
    print(f'\n>>> {descr}\n>>> {code}')
    

title('Retrieve first sys.argv or os.environ variable MY_DIR_PATH or None if not present',
      'dir_path = arg(1) or env("MY_DIR_PATH")')
dir_path = arg(1) or env('MY_DIR_PATH')
print(f'{dir_path = }')

title('Get remaining command line args beginning at arg(1)',
      'remaining_args = nargs(1)')
remaining_args = nargs(2)
print(f'{remaining_args = }')

title('Shift args',
      'removed = shift()); arg1 = arg(1)')
removed = shift()
arg1 = arg(1)
print(f'{removed = }  {arg1 = }')

title('Open the dir_path and verify it is a directory',
      'if Path(dir_path).expanduser().is_dir() else exit(2)')
if dir_path:
    my_dir = Path(dir_path).expanduser()
    if not my_dir.is_dir():
        print(f'Exiting: cannot find {dir_path}')
        exit(2)
else:
    print('usage: ./myscript dir_path') 
    print('       -- or -- ')
    print('       MY_DIR_PATH=~/git/pyscriptlib; ./myscript')
    exit(1)
print(f'{my_dir = }')


title('Capture the stripped output from stdout+stderr',
      'output = sh(cmd)')
output = sh(f'ls -alh {my_dir}')
print(output)


title('Execute the command directly sending output to the terminal',
      'shx(cmd)')
shx(f'tree {my_dir}')


title('Get a list of return values from subprocess.CompletedProcess object -- test with rc == 0',
      'rc, stdout, stderr = shl(cmd); if rc == 0:')
rc, stdout, stderr = shl(f'ls -alh {my_dir}')
if rc == 0:
    print(f'{rc = }\n{stdout = }')
else:
    print(f'{rc = }\n{stderr = }')


title('Get a list of return values from subprocess.CompletedProcess object -- test with boolean is_ok',
      'is_ok, rc, stdout, stderr = shk(cmd); if is_ok:')
is_ok, rc, stdout, stderr = shk(f'ls -alh {my_dir}')
if is_ok:
    print(f'{is_ok = } {rc = }\n{stdout = }')
else:
    print(f'{is_ok = } {rc = }\n{stderr = }')


title('Get the customized subprocess.CompletedProcess object -- test with boolean cp.is_ok',
      'cp = sho(cmd); if cp.is_ok:')
cmd = f'''
cd {my_dir}
grep -r \
    --exclude='*.pyc' \
    --exclude-dir='.git' --exclude-dir='dist' --exclude-dir='*.egg-info' \
    pyscriptlib
'''
print('cmd = ', cmd)
cp = sho(cmd)
if cp.is_ok:
    text = cp.stdout.splitlines()
    print(text)
else:
    print(f'grep failed: {cp.rc = } {cp.stderr = }')
    exit(cp.rc)


title('Create and kill background process with pid',
      'pid = shb(cmd); kill(pid)')
pid = shb(f'echo "hello from background process"; sleep 10')
print(f'{pid = }')
time.sleep(1)
kill(pid)


title('Humanize the uptime for this host',
      'uptimes = sh("cat /proc/uptime"); humanize(uptimes[0]))')
uptimes = sh('cat /proc/uptime')
if uptimes:
    uptime = float(uptimes.split(' ')[0]) 
    print(f'{humanize(uptime) = }')
    print(f'{humanize(uptime, style="full") = }')
```

### A Personal Note
I've been using `bash` for over 35 years (since the days of Bell Labs Unix where it was invented by Stephen Bourne), but I never really felt very confident with its (to me) arcane syntax. 

No, I don't mean just the things like this
```bash
# I'm not always sure which condition form to use 
# and watch those spaces around the brackets!!!  
# not to mention tests like -x, -n, -z and $? == 0 is success?

if <condition> | [ <condition> ] | [[ <condition> ]] 
then
    <statements>
else 
    <statements> 
fi

# seriously, );; );; esac anyone?

case <value> in 
    <match> ) <statements> ;;
    <match> ) <statements> ;;
    * ) <statements>;;
esac
```
But mostly the magic stuff you can do with array notation that is so cryptic it makes my eyes water. 

```bash
# I'm still not sure what all this means :-(

locations=( "New York" Chicago Atlanta Miami )
for val in ${!locations[@]}
do
   echo "index = ${val} , value = ${locations[$val]}"
done
```
Sigh, and I thought that `perl` was noisy ...

So I started looking for a better shell and what I actually found was ***python***. It's a more powerful interpreter with a much more comfortable and much less cryptic syntax than `bash`. 

Along the way, I also considered the python `conch` shell, but it wants to be a new hybrid language in a REPL, and I don't really want the overhead of another layer of shell even if it is `ipython` at its heart.

In particular, all I really want to do is easily invoke the `bash shell` to run useful tools like `grep`, `ls -alh`, `tree`, `ip address`, *et alia*, but otherwise I'm happy with python syntax as the medium in a script file.

Unfortunately, the down-side to using python for scripting is that it is still a real programming language -- so creating `bash equivalent` scripts can get a bit hairy, to say the least.

This is especially true when you start using `subprocess.Popen()` and its incredibly powerful capabilities to fork any process you want with any options you want. But the price of power can be overwhealming complexity.

And so, I finally realized that all I really need is a concise set of wrapper functions that I can use to embed `bash commands` in my python code and let them actually do all the heavy lifting using `subprocess.Popen()` -- and why not throw in some `sys` and `os` sugar as well? 

And, thus, complexity begat ***pyscriptlib*** and here we are.

### A Testimonial to pathlib.Path -- Can I have an Amen?
I am also highly impressed with the `Path` class from the standard `pathlib` module. The `Path` object model helps my python scripts become much more concise as I'm often navigating the file system such as `Path.home()/'subdir'` before I launch some `sh*(cmd)` that accesses the files. 

Ooh, ooh, Mr. Kotter: this is not a typo, rather, it is the coolest use of a class dunder method to create a `Path slash(/) join operator` that I have seen:
```python
# using the Path slash(/) join operator
file_path = Path.home() / 'subdir' / 'file'

# is the same as using the Path.joinpath() method
file_path = Path.home().joinpath('subdir', 'file')

# and the Path instance has direct access methods to the file system
if file_path.is_file():
  text = file_path.read_text()

# bang, zoom, that's all folks
```
The old way of doing this with `os.path` was only slightly less painful than `subprocess.Popen`. I leave that as a heartless exercise for the reader :-).
