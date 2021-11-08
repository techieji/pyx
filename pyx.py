__doc__ = "Manage and run anonymous, immutable virtual environments."
__version__ = "0.0.1"

import subprocess
import json
import sys
from pathlib import Path
import shutil
import os
import venv
import hashlib
import platform

try:
    from pip._internal.network.session import PipSession
    from pip._internal.req import parse_requirements
except ImportError:
    PipSession = lambda: error('Requirements parser could not be found.', 1)
    parse_requirements = lambda *a: error('Requirements parser could not be found.', 1)

IS_LINUX = platform.system() in ['Linux', 'Darwin']

if 'PATH_PREFIX' in os.environ:
    PATH_PREFIX = os.environ['PATH_PREFIX']
else:
    if platform.system() == 'Windows':
        PATH_PREFIX = Path(r'D:\Documents\Pradhyum\Git-Repos\pyx')
    else:
        PATH_PREFIX = Path('/mnt/d/Documents/Pradhyum/Git-Repos/pyx')    # temporary

def prompt(s, inp=True, default=None): return ((lambda *a: w if (w := input(*a)) and default is not None else default) if inp else print)(f"[\033[1;33mPROMPT\033[0m] {s}")
def debug(s): print(f'[\033[94mDEBUG\033[0m] {s}')
def info(s): print(f'[\033[92mINFO\033[0m] {s}')
def warning(s): print(f'[\033[93mWARNING\033[0m] {s}')
def error(s, exit_p=None):
    print(f'[\033[91mERROR\033[0m] {s}')
    if exit_p is not None: sys.exit(exit_p)

class Db:
    def __init__(self):
        info('Opening database')
        try:
            with open(PATH_PREFIX / 'db.json') as f:
                self.db = json.load(f)
        except FileNotFoundError:
            error('Database could not be found', 1)

    def save(self):
        with open(PATH_PREFIX / 'db.json', 'w') as f:
            json.dump(self.db, f)
        info('Saved to database')

    @staticmethod
    def set_to_string(l: frozenset):
        return '-'.join(sorted(l))

    def add_requirements(self, l: frozenset, d):
        self.db[Db.set_to_string(l)] = d

    def remove_env(self, packages):
        if type(packages) == frozenset:
            info(f'Deleting this package combination: {", ".join(packages)}')
            packages = get_name(packages)
        try:
            del self.db[packages]
        except KeyError:
            error(f'No such cache-location `{packages}`', 1)
        self.save()
        info(f'Deleted `{packages} from database`')
        prompt(f'Delete contents of {PATH_PREFIX / 'cache' / packages}? [Y/n]', default='y')
        try:
            shutil.rmtree(PATH_PREFIX / 'cache' / packages)
        except FileNotFoundError:
            error('Environment directory could not be found.', 1)
        info('Deleted environment directory')

def prefix_path(n):
    return PATH_PREFIX / 'cache' / n

def hex_hash(o):
    return hashlib.sha256(bytes('-'.join(o), encoding='utf-8')).hexdigest()[:8]

def get_name(s):
    h = hex_hash(s)
    return '-'.join([h] + list(s))

def copy_inve(name, path):
    with open(PATH_PREFIX / 'inve') as f: s = f.read()
    with open(path / 'bin' / 'inve', 'w')  as f: f.write(s.format(path))

def make_ive(name):
    file = prefix_path(name)
    venv.create(file)
    info(f'Created immutable environment `{name}`')
    return file

def make_ve(db, s):
    info('Checking database...')
    string = Db.set_to_string(s)
    if string in db.db:
        info('Found in database')
        res = db.db[string]
        info('Loaded from database')
        return Path(res)
    else:
        info('Not found in database')
        name = get_name(s)
        info('Creating immutable environment')
        file = make_ive(name)
        info('Installing packages')
        version_str = f'python{sys.version_info.major}.{sys.version_info.minor}'
        for x in s:
            subprocess.run([sys.executable, '-m', 'pip', 'install', x, f'--target={file}/lib/{version_str}/site-packages'], capture_output=True)
            info(f'Installed {x}')
        info('Created environment')
        db.add_requirements(s, str(file))
        db.save()
        return file

def main_make_ve(packages):
    a = frozenset(packages)
    debug("Hash: " + hex_hash(a))
    db = Db()
    d = make_ve(db, a)
    debug(f'Environment path: {d}')
    if platform.system() in ['Linux', 'Darwin']:
        copy_inve(get_name(a), d)
        info('Copied shell invoker to environment')
        info('Invoking shell...')
        if (d / 'bin').exists():
            os.system(f"{d / 'bin' / 'inve'}")
        else:
            prompt("This environment was created under Windows and thus doesn't contain", False)
            prompt("the proper binaries that Linux expects. Environments created under", False)
            r = prompt("Linux are compatible with Windows. Create a new environment? [Y\n] ", default='y').lower()
            if r == 'y':
                pass
    else:
        error('Systems other than Linux or Darwin are not supported. To enter the created')
        error('environment, run this command')
        error(f'    . {d}/Scripts/Activate.ps1')
        error('or, if the environment was made on Linux, this command:')
        error(f'    . {d}/bin/Activate.ps1')
        error('This shortfall will be fixed in the future.', 0)

def main_requirements():
    info('Loading packages from requirements.txt')
    reqs = parse_requirements('requirements.txt', session=PipSession())
    info(f'Parsed requirements.txt ({len(reqs)} package{"s" if len(reqs) > 1 else ""})')
    main_make_ve(reqs)

def main():
    a = sys.argv[1:]
    if a:
        main_make_ve(a)
    elif Path('requirements.txt') in Path('.').iterdir():
        main_requirements()
    else:
        error('Please provide at least one package')
        sys.exit(1)

if __name__ == '__main__':
    main()
