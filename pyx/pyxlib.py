import venv
import sys
import os
from pathlib import Path
from phash import phash
from subprocess import run

CACHE_DIR = Path('/c/Users/1593179/Documents/pyx/cache')

class Package:
    def __init__(self, name, version):
        self.name = name
        self.version = version
        if not self.installed:
            self.install()

    def __str__(self):
        return f'{phash(self.name + str(self.version))}-{self.name}-{self.version}'

    @property
    def installed(self):
        return CACHE_DIR.contains(str(self))

    def _get_dir(self):
        v = 'python' + ".".join(map(str, sys.version_info[:2]))
        return CACHE_DIR / str(self) / 'lib' / v / 'site-packages'

    def install(self):
        venv.create(CACHE_DIR / str(self), prompt='(pyx) ')
        run([sys.executable, '-m', 'pip', 'install', f'{self.name}=={self.version}', f'--target={self._get_dir()}'], check=True)
    
    @staticmethod
    def make_entry_script(ps):
        os.system(';'.join(map(f'source {CACHE_DIR}/{{}}', map(str, ps))) + ';' + 'bash')
