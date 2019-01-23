from pprint import pprint

import tox
import tox.venv


# This will store the pip version specified for each testenv
PER_ENV_PIP_VERSIONS = {}


@tox.hookimpl
def tox_configure(config):
    for env, envconfig in config.envconfigs.items():
        pip_version = envconfig._reader.getstring("pip_version")
        PER_ENV_PIP_VERSIONS[env] = pip_version


@tox.hookimpl
def tox_testenv_create(venv, action):
    tox.venv.tox_testenv_create(venv, action)
    # action.venvname is 'py36', for example
    # I see action.id == action.venvname - not sure which to use
    pip_version = PER_ENV_PIP_VERSIONS.get(action.venvname)
    if pip_version:
        print('%s: pip_version = %s' % (action.venvname, pip_version))
        package = 'pip==%s' % pip_version
        # "private" _install method - unstable interface?
        venv._install([package], extraopts=['-U'], action=action)
    return True
