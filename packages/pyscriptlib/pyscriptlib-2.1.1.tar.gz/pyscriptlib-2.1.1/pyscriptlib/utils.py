"""
Python Bash Script Helper Utilties

Shell commands require *nix with bash shell
"""
import sys, os
import subprocess as sp


def arg(n:int):
    """Retrieve command line arg by index

    Args:
        n (int): arg index

    Returns:
        str: arg value or null string
    """
    return sys.argv[n] if len(sys.argv) >= n+1 else ''

def nargs(n:int):
    """Retrieve remaining command line args starting at index

    Args:
        n (int): beginning arg index

    Returns:
        list: arg values or []
    """
    return sys.argv[n:]


def shift(n:int=1):
    """Shift command line args by n, preserving sys.argv[0]

    Args:
        n (int): number of args to remove from sys.argv
    
    Returns: list of args removed
    """
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    removed = args[:n]
    
    sys.argv = [sys.argv[0]] + args[n:]
    
    return removed
        
def exit(return_code:int=0):
    """Ext the script with return code

    Args:
        code (int, optional): return code. Defaults to 0.
    """
    sys.exit(return_code)


def env(var:str):
    """Retrieve OS environment variable by name

    Args:
        var (str): Env variable name

    Returns:
        str: Env variable value or None
    """
    return os.environ.get(var, None)

def kill(pid:int, signal:int=9):
    """Kill the process for this pid

    Args:
        pid (int): process-id to kill
        signal (int, optional): signal used to kill the process. Defaults to 9.
    """
    os.kill(pid, signal)
    

def sh(cmd:str, **kwargs):
    """Return captured result from bash shell command as stripped stdout+stderr

    Args:
        cmd (str): Command string
        **kwargs: additional args for subprocess.run()

    Returns:
        str: stripped stdout + stderr
    """
    cp = sp.run(cmd, shell=True, executable='/bin/bash', 
                text=True, stdout=sp.PIPE, stderr=sp.PIPE, **kwargs)
    result = cp.stdout + cp.stderr
    return result.strip()

def shl(cmd:str, **kwargs):
    """Return list from bash shell command as [returncode, stdout, stderr]

    Args:
        cmd (str): Command string
        **kwargs: additional args for subprocess.run()

    Returns:
        int: returncode
        str: stdout (raw)
        str: stderr (raw)
    """
    cp = sp.run(cmd, shell=True, executable='/bin/bash', 
                text=True, stdout=sp.PIPE, stderr=sp.PIPE, **kwargs)
    return cp.returncode, cp.stdout, cp.stderr

def shk(cmd:str, **kwargs):
    """Return list from bash shell command as [is_ok, returncode, stdout, stderr]

    Args:
        cmd (str): Command string
        **kwargs: additional args for subprocess.run()

    Returns:
        bool: is_ok: True if returncode == 0
        int: returncode
        str: stdout (raw)
        str: stderr (raw)
    """
    cp = sp.run(cmd, shell=True, executable='/bin/bash', 
                text=True, stdout=sp.PIPE, stderr=sp.PIPE, **kwargs)
    is_ok = cp.returncode == 0
    return is_ok, cp.returncode, cp.stdout, cp.stderr

def sho(cmd:str, **kwargs):
    """Return CompletedProcess object from bash shell command

    Args:
        cmd (str): Command string
        **kwargs: additional args for subprocess.run()

    Returns:
        CompletedProcess object:
        - cp.is_ok: True if cp.rc == 0
        - cp.rc or cp.returncode
        - cp.stdout
        - cp.stderr
    """
    cp = sp.run(cmd, shell=True, executable='/bin/bash', 
                text=True, stdout=sp.PIPE, stderr=sp.PIPE, **kwargs)
    # set alias cp.rc and cp.is_ok
    cp.rc = cp.returncode
    cp.is_ok = cp.returncode == 0
    return cp

def shx(cmd:str, **kwargs):
    """Run command via bash shell with no return but real-time results spill to the terminal

    Args:
        cmd (str): Command string
        **kwargs: additional args for subprocess.run()
    """
    # let the command run and spill to the screen
    sp.run(cmd, shell=True, executable='/bin/bash', **kwargs)

def shb(cmd:str, **kwargs)->int:
    """Run command via bash shell in the background returning the pid
    
    Args:
        cmd (str): Command string
        **kwargs: additional args for subprocess.run()
    """
    # run this command in bash in the background returning the pid
    p = sp.Popen(cmd, shell=True, executable='/bin/bash', close_fds=True, **kwargs)
    return p.pid


def humanize(seconds:int|float, style='compact', days='days', zerodays=True):
    """Format humanized elapsed seconds as
        - compact style: 'DD {days} HH:MM:SS'
        - full style: 'DD{days[0]} HHh MMm SSs'

    Args:
        seconds (int|float): seconds to humanize
        style (str):         'compact' => default compact format, 'full' => full format 
        days (str):          days label => default 'days'
        zerodays (bool):     show zero days => default True, False => suppress zero days

    Returns:
        str: human formatted string 'full'=>`'05 days 03:59:27'` or 'compact'=>`'05d 03h 59m 27s'`
    """
    # parse the seconds
    dd = int(seconds / 86400)
    hh = int(seconds % 86400 / 3600)
    mm = int(seconds % 3600 / 60)
    ss = int(seconds % 60)    

    if style == 'compact':
        dds = f'{dd:02d} {days} '
        if not zerodays and dd == 0:
            dds = ''
        return f'{dds}{hh:02d}:{mm:02d}:{ss:02d}'
    elif style == 'full':
        return f'{dd:02d}{days[0]} {hh:02d}h {mm:02d}m {ss:02d}s'
    else:
        return f'{seconds} seconds'
    

def test():
    import time
    sys.argv += ['arg1', 'arg2']
    print(f'{arg(1) = }  {arg(2) = }')
    print(f'{shift(1) = }  {arg(1) = }')
    print(f'{shift(2) = }  {arg(1) = }')
    
    print(f"{sh('ls') = }")
    print(f"{shl('ls') = }")
    print(f"{shk('ls') = }")
    
    cp = sho('ls')
    print(f"sho('ls'): {cp.args = } {cp.is_ok = } {cp.rc = }  {cp.stdout = }  {cp.stderr = }")

    cp = sho('ls xxx')
    print(f"sho('ls xxx'): {cp.args = } {cp.is_ok = } {cp.rc = }  {cp.stdout = }  {cp.stderr = }")

    print(f"shx(ls -alh)")
    shx('ls -alh')

    pid = shb('sleep 200')
    print(f"pid = shb('sleep 200'); {pid = }")
    time.sleep(1)
    print(f"{kill(pid) = }")

    print()
    print(f"{humanize(time.time()) = }")
    print(f"{humanize(time.time(), 'full') = }")
    print(f"{humanize(time.time(), 'full', zerodays=False) = }")
    
    print(f"{humanize(200) =}")
    print(f"{humanize(200, zerodays=False) = }")
    print(f"{humanize(200, 'full') = }")
    print(f"{humanize(200, 'full', zerodays=False) = }")

    print('\nexit(1)')
    exit(1)
    
if __name__ == '__main__':
    test()
