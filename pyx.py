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
from argparse import ArgumentParser

def debug(s):
    print(f'[\033[94mDEBUG\033[0m] {s}')

def info(s):
    print(f'[\033[92mINFO\033[0m] {s}')

def warning(s):
    print(f'[\033[93mWARNING\033[0m] {s}')

def error(s, exit_p=0):
    print(f'[\033[91mERROR\033[0m] {s}')
    if exit_p != 0:
        sys.exit(exit_p)

class Db:
    def __init__(self):
        info('Opening database')
        try:
            with open('db.json') as f:
                self.db = json.load(f)
        except FileNotFoundError:
            error('Database could not be found', 1)

    def save(self):
        with open('db.json', 'w') as f:
            json.dump(self.db, f)
        info('Saved to database')

    @staticmethod
    def set_to_string(l: frozenset):
        return '-'.join(sorted(l))

    def add_requirements(self, l: frozenset, d):
        self.db[Db.set_to_string(l)] = d

def prefix_path(n):
    return Path(__file__).parent / 'cache' / n

def hex_hash(o):
    return hashlib.sha256(bytes('-'.join(o), encoding='utf-8')).hexdigest()[:8]

def get_name(s):
    h = hex_hash(s)
    return '-'.join([h] + list(s))

def copy_inve(name, path):
    with open(Path(__file__).parent / 'inve') as f: s = f.read()
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
        for x in s:
            subprocess.run([sys.executable, '-m', 'pip', 'install', x, f'--target={file}/lib/python3.9/site-packages'], capture_output=True)
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
    copy_inve(get_name(a), d)
    info('Copied shell invoker to environment')
    info('Invoking shell...')
    os.system(f"{d / 'bin' / 'inve'}")

def main():
    a = sys.argv[1:]
    if a:
        main_make_ve(a)
    elif Path('requirements.txt') in Path('.').iterdir():
        info('Would install from requirements (NOT IMPLEMENTED)')
    else:
        error('Please provide at least one package')
        sys.exit(1)

if __name__ == '__main__':
    main()
