[![Build Status](https://travis-ci.com/pglass/tox-pip-version.svg?branch=master)](https://travis-ci.com/pglass/tox-pip-version)
![](https://img.shields.io/pypi/v/tox-pip-version.svg)
![](https://img.shields.io/pypi/pyversions/tox-pip-version.svg)

**Deprecated**: With virtualenv version 20+, virtualenv supports installing a specific
version of pip as part of virtualenv creation. **The `tox-pip-version` plugin is no longer
required and is therefore deprecated.**

Here is an example of installing a specific version of pip with tox:

```ini
[tox]
envlist = py36
minversion = 3.10.0  # Ensure the `download` option is supported
requires = virtualenv >= 20.0
skipsdist = True

[testenv]
download = true
setenv =
    VIRTUALENV_PIP=19.2.3
    VIRTUALENV_SEEDER=pip
    VIRTUALENV_DOWNLOAD=1
```

For those currently using tox-venv, simply specify `VIRTUALENV_CREATOR=venv`
as an additional environment variable.

Overview
--------

This is a tox plugin that preinstalls a specific version of pip in each tox
environment.

```bash
pip install tox-pip-version
```

This works around the default behavior of tox/virtualenv that always installs
the latest version pip. It is an improvment over the `VIRTUALENV_NO_DOWNLOAD=1`
option that does not install the latest version, but could result in usage of
an outdated version of pip.

*Recommendation*: Do not pin the pip version long term. You get more stable
repeatable builds, but at the cost of using an outdated (possibly vulnerable)
package. This should be used as a temporary fix for breakages in upstream pip,
or in conjunction with a regular process to update the version pin.

*Note*: This relies on an [unstable tox plugin interface](
https://tox.readthedocs.io/en/latest/plugins.html#tox.hookspecs.tox_testenv_create).
You may experience breakage with new tox versions. If you do, please feel
free to [report the issue](https://github.com/pglass/tox-pip-version/issues/new)
on Github.

### Usage

Install the package and include `pip_version` in your tox.ini

```tox
[testenv]
pip_version = pip==19.0.1
```

Or, set the `TOX_PIP_VERSION` environment variable,

```bash
export TOX_PIP_VERSION=18.1
tox
```

The plugin will install that version of pip into the tox-created virtualenv,
just after tox creates the virtualenv, but before dependencies are installed.

The `pip_version` within tox.ini, if present, is always used over the
environment variable.

If neither `pip_version` or `TOX_PIP_VERSION` is present, the plugin does
nothing.

### Version Sets

Version sets/ranges are supported, enabling installation of a version of pip
matching a set of specifiers. There are two basic formats: a plain version
number, or the package name with optional [PEP440-compatible](
https://www.python.org/dev/peps/pep-0440/#version-specifiers) version
specifiers.

| tox.ini                      | effective pip command        |
| ---------------------------- | ---------------------------- |
| `pip_version = 19.0`         | `pip install -U pip==19.0`   |
| `pip_version = pip==19.0`    | `pip install -U pip==19.0`   |
| `pip_version = pip>=19.0`    | `pip install -U pip>=19.0`   |
| `pip_version = pip!=19,>18`  | `pip install -U pip!=19,>18` |
| `pip_version = pip`          | `pip install -U pip`         |

### Tests

Use `make test` to run the tests, which includes linting and functional tests.

Each of the `tests/*` directories is a "feature" that needs testing. Each
feature sub-directory contains a tox.ini file that sets pip version in a
particular way, and then uses a tox command to check the correct pip version
was installed.
