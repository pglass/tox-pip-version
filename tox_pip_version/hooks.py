import os

import tox
import tox.venv


# This will store the pip version specified for each testenv
PER_ENV_PIP_VERSIONS = {}

TOX_PIP_VERSION_VAR = "TOX_PIP_VERSION"


def _testenv_create(venv, action):
    # For compatibility with the tox-venv plugin:
    #
    # - detect if tox-venv is installed and invoke if so
    # - use `tryfirst=True` on our hookimpl to run before tox-venv does (no
    #   more plugins after a plugin returns non-None from its hook function)
    try:
        from tox_venv.hooks import tox_testenv_create
    except ImportError:
        from tox.venv import tox_testenv_create
    tox_testenv_create(venv, action)


@tox.hookimpl
def tox_configure(config):
    for env, envconfig in config.envconfigs.items():
        pip_version = envconfig._reader.getstring("pip_version")
        if pip_version:
            PER_ENV_PIP_VERSIONS[env] = pip_version


@tox.hookimpl(tryfirst=True)
def tox_testenv_create(venv, action):
    _testenv_create(venv, action)

    # Grab the env this way to respect `setenv = TOX_PIP_VERSION`, if present.
    # But, fallback to the process-level environment if not present in `setenv`
    env = venv._get_os_environ()
    tox_pip_version_from_env = env.get(
        TOX_PIP_VERSION_VAR, os.getenv(TOX_PIP_VERSION_VAR)
    )

    # action.venvname is 'py36', for example.
    #
    # tox 3.8 changed action.venvname -> action.name, and removed action.id
    try:
        venvname = action.venvname
    except AttributeError:
        venvname = action.name

    # Use `pip_version` in tox.ini over the environment variable
    pip_version = PER_ENV_PIP_VERSIONS.get(venvname, tox_pip_version_from_env)
    if pip_version:
        # Is there a way to output this better? Genuine tox commands show up
        # colorized (as bold white text)...
        print("%s: pip_version = %s" % (venvname, pip_version))
        package = "pip==%s" % pip_version

        # "private" _install method - unstable interface?
        venv._install([package], extraopts=["-U"], action=action)
    return True
