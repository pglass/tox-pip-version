import itertools
import os
import subprocess
import sys

if sys.version_info.major == 2:
    from backports import tempfile
else:
    import tempfile

import pytest

HERE = os.path.realpath(os.path.dirname(__file__))
PACKAGE_DIR = os.path.realpath(os.path.join(HERE, '..'))

TOX_VERSIONS = [
    ">=3.7,<3.8",
    ">=3.8,<3.9",
]

TOX_TO_TOX_VENV_VERSIONS = {
    # tox-venv 0.4.0 requires tox>=3.8.1
    ">=3.7,<3.8": "<0.4.0",
    ">=3.8,<3.9": ">=0.4.0",
}

CASES = {
    "test-two-envs": {
        "env": {},
    },
    "test-env-inheritance": {
        "env": {},
    },
    "test-environment-variable": {
        "env": {"TOX_PIP_VERSION": "18.1"},
    },
}

PYTEST_PARAMETERS = sorted(itertools.product(TOX_VERSIONS, CASES))


def setup_fresh_venv(tag, *extra_commands):
    temp_dir = tempfile.TemporaryDirectory(prefix=tag)
    venv_dir = os.path.join(temp_dir.name, 'venv')
    subprocess.check_call(["virtualenv", venv_dir])
    print('Created venv: %s' % venv_dir)
    return temp_dir, venv_dir


def install_deps(venv_dir, *deps):
    """Install a dependency into the virtualenv"""
    pip = os.path.join(venv_dir, 'bin', 'pip')
    cmd = [pip, "install"] + list(deps)
    subprocess.check_call(cmd, cwd=venv_dir, env={})


def _run_case(venv_dir, subdirectory, env=None):
    tox_work_dir = os.path.join(venv_dir, '.tox')
    directory = os.path.join(HERE, subdirectory)
    activate = os.path.join(venv_dir, 'bin', 'activate')
    command = '. %s; pip freeze; tox --workdir %s' % (activate, tox_work_dir)
    print("Running: '%s'" % command)
    subprocess.check_call(command, cwd=directory, shell=True, env=env or {})


@pytest.mark.parametrize("tox_version,subdirectory", PYTEST_PARAMETERS)
def test_with_tox_version(tox_version, subdirectory):
    env = CASES[subdirectory]['env']
    temp_dir, venv_dir = setup_fresh_venv(tag=subdirectory)
    try:
        # Sometimes see an error like,
        #
        #    Could not find a version that satisfies the requirement
        #    tox<3.8,>=3.7 (from versions: none)
        #
        # Trying separate install commands due to suspicion that the directory
        # installation is what causes this. tox-pip-version has `tox>=2.0` and
        # we install something like `tox<3.8,>=3.7`. Maybe that combo causes
        # some sort of issue?
        install_deps(venv_dir, "tox%s" % tox_version)
        install_deps(venv_dir, PACKAGE_DIR)
        _run_case(venv_dir, subdirectory, env=env)
    finally:
        temp_dir.cleanup()


@pytest.mark.parametrize("tox_version,subdirectory", PYTEST_PARAMETERS)
def test_with_tox_version_with_tox_venv(tox_version, subdirectory):
    env = CASES[subdirectory]['env']
    tox_venv_version = TOX_TO_TOX_VENV_VERSIONS[tox_version]

    temp_dir, venv_dir = setup_fresh_venv(tag=subdirectory)
    try:
        install_deps(
            venv_dir, "tox%s" % tox_version, "tox-venv%s" % tox_venv_version
        )
        install_deps(venv_dir, PACKAGE_DIR)
        _run_case(venv_dir, subdirectory, env=env)
    finally:
        temp_dir.cleanup()
