import pyxlib
import sys
from pip._internal.req import parse_requirements

l = parse_requirements(sys.argv[1] if sys.argv[1:] else 'requirements.txt', session=False)
ps = [pyxlib.Package(x.requirement) for x in l]
pyxlib.Package.open_shell_with(ps)
