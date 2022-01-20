import sys
import os
from pathlib import Path
from phash import phash
from subprocess import run
from spinny import Spinner
import re

CACHE_DIR = Path.home() / '.pyx'
if not CACHE_DIR.exists():
    CACHE_DIR.mkdir(parents=True)

class Package:
    def __init__(self, name):
        self._name = name
        self.name = re.match(r'\w+', self._name).group(0)
        if not self.installed:
            self.install()
        else:
            print(f'\r\033[0;32m✓\033[0m {self.name} already installed')

    def __str__(self):
        return f'{phash(self.name)}-{self.name}'

    @property
    def installed(self):
        return CACHE_DIR.joinpath(str(self)).exists()

    @property
    def location(self):
        return CACHE_DIR.joinpath(str(self))

    def install(self):
        self.location.mkdir()
        with Spinner(f"Installing {self.name}", f'Installed {self.name}'):
            run([sys.executable, '-m', 'pip', 'install', f'{self._name}', f'--target={self.location}'], check=True, capture_output=True)
 
    @staticmethod
    def open_shell_with(ps):
        os.environ['PYTHONPATH'] = ':'.join(str(x.location) for x in ps)
        os.environ['PS1'] = '(\033[31mpyx\033[0m) ' + os.environ['PS1']
        os.system(os.environ['SHELL'])
