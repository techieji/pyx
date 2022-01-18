import subprocess
import shutil
import sys
import os
from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements
from shutil import copy2
from phash import phash

# SLog (Short Logger), logs to stdout.
# globals().update({t:(lambda t,c:lambda m:print(f'[\033[{c}m{t.upper()}\033[0m] {m}'))(t,c)for t,c in{'error':31,'env':32,'package':33,'info':34}.items()})

mk_log = lambda t, c: lambda m: print(f'[\033[{c}m{t.upper()}\033[0m] {m}')
error = mk_log('error', 31)
env = mk_log('env', 32)
package = mk_log('package', 33)
info = mk_log('info', 34)

inve = r"""
export VIRTUAL_ENV="{}"
export PS1="\n\e[0;32m[pyx-shell:\w]\$\e[0m "
export PATH="$VIRTUAL_ENV/bin:$PATH"
unset PYTHON_HOME
exec "${{@:-$SHELL}}"
"""

class Env:
    def __init__(self, d, ps):
        self.d = d
        self.ps = sorted(ps)

    @property
    def phash(self):
        return phash(' '.join(self.ps))

    @property
    def venv_directory(self):
        return os.path.join(self.d, '.pyx', self.phash)

    @staticmethod
    def get_reqs(d, name='requirements.txt'):
        file = os.path.join(d, name)
        info(f"Parsing requirements ({os.path.relpath(file)})")
        if not os.path.exists(file):
            error('No requirements found')
            sys.exit(1)
        return [str(x.requirement) for x in parse_requirements(file, session=PipSession())]

    def _make_venv(self):
        info('Creating empty environment')
        try:
            subprocess.run([sys.executable, "-m", "venv", self.venv_directory, "--without-pip"], check=True)
        except subprocess.CalledProcessError:
            error("Venv could not be created.")
            sys.exit(2)
        v = ".".join(map(str, sys.version_info[:2]))
        info('Installing packages')
        for p in self.ps:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', p, f'--target={self.venv_directory}/lib/python{v}/site-packages'], capture_output=True, check=True)
            except subprocess.CalledProcessError:
                error(f"{p} could not be installed")
            else:
                package(f"Installed {p}")
        with open(os.path.join(self.venv_directory, 'inve'), 'w', encoding='utf-8') as f:
            f.write(inve.format(self.venv_directory))
        info("Entry script written")
        copy2(os.path.join(self.d, 'requirements.txt'), self.venv_directory)
        info("Froze requirements.txt")


    def make_venv(self):
        if not os.path.exists(new_path := os.path.join(self.d, '.pyx')):
            os.mkdir(new_path)
            info('Created environment store')
        if not os.path.exists(self.venv_directory):
            self._make_venv()
        else:
            info('Reusing cached environment')

    def open_venv(self, direct=False):
        info('Opening environment')
        subprocess.run(['sh', os.path.join(self.d if direct else self.venv_directory, 'inve')], check=True)
        print()

    def delete(self, direct=False):
        shutil.rmtree(self.d if direct else self.venv_directory)

    @staticmethod
    def from_directory(d, name='requirements.txt'):
        return Env(d, Env.get_reqs(d, name))

    @staticmethod
    def all_envs(_d):
        d = os.path.join(_d, '.pyx')
        return [Env.from_directory(os.path.join(d, x)) for x in os.listdir(d)]

    @staticmethod
    def search(ph, d):
        for x in Env.all_envs(d):
            if x.phash == ph:
                return x
        error(f'Environment {ph} not found')
        sys.exit(1)

def main():
    info("Constructing environments from requirements.txt")
    e = Env.from_directory(os.getcwd())
    e.make_venv()
    e.open_venv()

if __name__ == '__main__':
    main()
