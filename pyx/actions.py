from pyxlib import Env, env

def get_info(d):
    envs = Env.all_envs(d)
    env("Listing environments:")
    for x in envs:
        env(f" • {x.phash}: {', '.join(x.ps)}")

def open_env(ph, d):
    Env.search(ph, d).open_venv(direct=True)

def delete(ph, d):
    Env.search(ph, d).delete(direct=True)
