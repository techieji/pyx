# Pyx

*Environment management made easy*

**Note: since this project is being actively developed, the information below may be out of date.**

Pyx exists to literally fit into any projects with a `requirements.txt` and make hacking on
it as simple as possible. By using virtualenv, Pyx is a fast and simple way to setup
environments. Here's an example:

```bash
$ cat requirements.txt
bottle
toolz
$ pyx
[INFO] A few steps occur...
[PACKAGE] Installed bottle
[PACKAGE] Installed toolz
[INFO] Two other steps occur...
[pyx-shell:] python3 -c "import bottle, toolz"
[pyx-shell:]
```

Reusing that environment is instant. And since it doesn't delete old environments unless asked
to, rolling back to a previous version is easy. Run `pyx help` for more info.

## Installing

Pyx is not available on Pypi yet, but that doesn't mean it isn't easy to install. Clone this
repository, run `make` (or don't, there should be a built executable in the path anyways), and
add `pyx/bin` to path. And you're done! That's basically the build process too.
