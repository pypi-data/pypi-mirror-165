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

title('Get remaining args',
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
