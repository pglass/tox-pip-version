import os

import tox
import tox.venv


# This will store the setuptools version specified for each testenv
PER_ENV_SETUPTOOLS_VERSIONS = {}

TOX_SETUPTOOLS_VERSION_VAR = "TOX_SETUPTOOLS_VERSION"


def _testenv_create(venv, action):
    # For compatibility with the tox-venv and tox-conda plugins:
    #
    # 1. Detect if tox-venv is installed and invoke if so.
    # 2. Else, detect if tox-conda is installed and invoke if so
    # 3. Else, neither is installed, so proceed as normal
    #
    # We use `tryfirst=True` on our hookimpl to run before tox-venv does (no
    # plugins run after a plugin returns non-None from its hook function)
    try:
        from tox_venv.hooks import tox_testenv_create

        # tox-venv may not create the venv (like if the venv is python 2)
        if tox_testenv_create(venv, action):
            return
    except ImportError:
        pass

    try:
        from tox_conda.plugin import tox_testenv_create

        if tox_testenv_create(venv, action):
            return
    except ImportError:
        pass

    tox.venv.tox_testenv_create(venv, action)


def get_setuptools_package_version(setuptools_version):
    setuptools_version = setuptools_version.lower().strip()
    # tox.ini: setuptools_version = setuptools==19.0
    if setuptools_version.startswith("setuptools"):
        return setuptools_version
    # tox.ini: setuptools_version = 19.0
    return "setuptools==%s" % setuptools_version


@tox.hookimpl
def tox_configure(config):
    for env, envconfig in config.envconfigs.items():
        setuptools_version = envconfig._reader.getstring("setuptools_version")
        if setuptools_version:
            PER_ENV_SETUPTOOLS_VERSIONS[env] = setuptools_version


@tox.hookimpl(tryfirst=True)
def tox_testenv_create(venv, action):
    _testenv_create(venv, action)

    # Grab the env this way to respect `setenv = TOX_SETUPTOOLS_VERSION`, if present.
    # But, fallback to the process-level environment if not present in `setenv`
    env = venv._get_os_environ()
    tox_setuptools_version_from_env = env.get(
        TOX_SETUPTOOLS_VERSION_VAR, os.getenv(TOX_SETUPTOOLS_VERSION_VAR)
    )

    # action.venvname is 'py36', for example.
    #
    # tox 3.8 changed action.venvname -> action.name, and removed action.id
    try:
        venvname = action.venvname
    except AttributeError:
        venvname = action.name






    # Use `setuptools_version` in tox.ini over the environment variable
    setuptools_version = PER_ENV_SETUPTOOLS_VERSIONS.get(
        venvname, tox_setuptools_version_from_env
    )
    if setuptools_version:
        package = get_setuptools_package_version(setuptools_version)

        # Is there a way to output this better? Genuine tox commands show up
        # colorized (as bold white text)...
        print("%s: setuptools_version is %s" % (venvname, package))

        # "private" _install method - unstable interface?
        venv._install([package], extraopts=["-U"], action=action)
    return True
