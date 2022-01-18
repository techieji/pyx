import os
import sys
from pyxlib import Env, info, error
from actions import get_info, open_env, delete

if sys.argv[1:]:
    if sys.argv[1] == 'info':
        get_info(os.getcwd())
    elif sys.argv[1] == 'help':
        print("""usage: pyx command [optional_args]

Available commands are:
    info: print out environments stored in the current directory
    help: print out this help message
    open: open an environment from a hash
    rm: remove an environment
    new: create an environment from a specified requirements file

All environments are stored in the .pyx directory. Pyx is pretty
resilient to changes in this directory, but not in each environment
itself. Environments can be removed manually and created manually
(provided it has the correct hash).
""")
    else:
        try:
            if sys.argv[1] == 'open':
                open_env(sys.argv[2], os.getcwd())
            elif sys.argv[1] == 'rm':
                delete(sys.argv[2], os.getcwd())
            elif sys.argv[1] == 'new':
                e = Env.from_directory(os.getcwd(), sys.argv[2])
                e.make_venv()
                e.open_venv()
        except IndexError:
            error("Not enough arguments")
            sys.exit(1)
else:
    info("Constructing environments from requirements.txt")
    e = Env.from_directory(os.getcwd())
    e.make_venv()
    e.open_venv()
