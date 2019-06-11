import itertools
import os
import subprocess
import tempfile

import pytest

HERE = os.path.realpath(os.path.dirname(__file__))
PACKAGE_DIR = os.path.realpath(os.path.join(HERE, '..'))

TOX_VERSIONS = [
    ">=3.7,<3.8",
    ">=3.8,<3.9",
]

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


def setup_fresh_venv(tag, *extra_commands):
    temp_dir = tempfile.TemporaryDirectory(prefix=tag)
    venv_dir = os.path.join(temp_dir.name, 'venv')
    p = subprocess.Popen(["virtualenv", venv_dir])
    p.wait()
    assert p.returncode == 0, "Failed to create venv in '%s'" % venv_dir
    return temp_dir, venv_dir


def install_dep(venv_dir, deps):
    """Install a dependency into the virtualenv"""
    pip = os.path.join(venv_dir, 'bin', 'pip')
    p = subprocess.Popen([pip, "install", deps], cwd=venv_dir, env={})
    p.wait()
    assert p.returncode == 0, "Failed to install deps: '%s'" % deps


def _run_case(venv_dir, subdirectory, env=None):
    tox_work_dir = os.path.join(venv_dir, '.tox')
    directory = os.path.join(HERE, subdirectory)
    activate = os.path.join(venv_dir, 'bin', 'activate')
    command = '. %s; pip freeze; tox --workdir %s' % (activate, tox_work_dir)
    print("Running: '%s'" % command)
    p = subprocess.Popen(
        command,
        cwd=directory,
        shell=True,
        env=env or {},
    )
    p.wait()
    assert p.returncode == 0, "Failure in directory '%s'" % directory


@pytest.mark.parametrize(
    "tox_version,subdirectory",
    list(itertools.product(TOX_VERSIONS, CASES.keys()))
)
def test_with_tox_version(tox_version, subdirectory):
    env = CASES[subdirectory]['env']

    temp_dir, venv_dir = setup_fresh_venv(tag=subdirectory)
    try:
        install_dep(venv_dir, "tox%s" % tox_version)
        install_dep(venv_dir, "%s" % PACKAGE_DIR)
        _run_case(venv_dir, subdirectory, env=env)
    finally:
        temp_dir.cleanup()


@pytest.mark.parametrize(
    "tox_version,subdirectory",
    list(itertools.product(TOX_VERSIONS, CASES.keys()))
)
def test_with_tox_version_with_tox_venv(tox_version, subdirectory):
    env = CASES[subdirectory]['env']

    temp_dir, venv_dir = setup_fresh_venv(tag=subdirectory)
    try:
        install_dep(venv_dir, "tox%s" % tox_version)
        install_dep(venv_dir, "%s" % PACKAGE_DIR)
        install_dep(venv_dir, "tox-venv")
        _run_case(venv_dir, subdirectory, env=env)
    finally:
        temp_dir.cleanup()


