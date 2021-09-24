import os
import pytest
import subprocess
import tempfile

HERE = os.path.realpath(os.path.dirname(__file__))
PACKAGE_DIR = os.path.realpath(os.path.join(HERE, ".."))

def setup_fresh_venv(tag):
    temp_dir = tempfile.TemporaryDirectory(prefix=tag)
    venv_dir = os.path.join(temp_dir.name, "venv")
    subprocess.check_call(["virtualenv", venv_dir])
    print("Created venv: %s" % venv_dir)
    return temp_dir, venv_dir


def install_deps(venv_dir, *deps):
    """Install a dependency into the virtualenv"""
    pip = os.path.join(venv_dir, "bin", "pip")
    cmd = [pip, "install"] + list(deps)
    subprocess.check_call(cmd, cwd=venv_dir, env={})


def _run_case(venv_dir, subdirectory, env=None):
    tox_work_dir = os.path.join(venv_dir, ".tox")
    directory = os.path.join(HERE, subdirectory)
    activate = os.path.join(venv_dir, "bin", "activate")
    command = ". %s; pip freeze; tox --workdir %s" % (activate, tox_work_dir)
    print("Running: '%s'" % command)
    subprocess.check_call(command, cwd=directory, shell=True, env=env)


## List test cases (which match tests sub-directory) and possibly add some environment variables
CASES = {
    "test-two-envs": {},
    "test-env-inheritance": {},
    "test-environment-variable": {
        "env": {"TOX_SETUPTOOLS_VERSION": "58.0.0"},
    },
    "test-version-specifiers": {}
}

@pytest.mark.parametrize("case", CASES)
def test_with_tox_version(case):
    """
    Tests our plugin outside of all other plugin and/or other framework.

    :param case: Test case to run
    :return:
    """
    env = case.get("env", default={})
    temp_dir, venv_dir = setup_fresh_venv(tag=case)
    try:
        install_deps(venv_dir, "tox")
        install_deps(venv_dir, PACKAGE_DIR)
        _run_case(venv_dir, case, env=env)
    finally:
        temp_dir.cleanup()

## Add one case when using tox_pip_version
CASES["test_with_airflow"] = {
    "env": {
        "TOX_SETUPTOOLS_VERSION": "58.0.0",
        "TOX_PIP_VERSION": "20.2.4",
    },
}

@pytest.mark.parametrize("case", CASES)
def test_with_tox_version_with_tox_pip_version(case):
    """
    Test our plugin when using in combination with tox-pip-version.

    At the very first version it didn't work very well because of some bad interaction issues (because we were implementing the same tox hook)

    This tests are able to install airflow (which was the root cause of this plugin)
    :param case: test case to run
    :return: Nothin, just run the tests
    """
    env = case.get("env", default={})
    env["TOX_PIP_VERSION"] = "20.2.4"

    temp_dir, venv_dir = setup_fresh_venv(tag=case)
    try:
        install_deps(venv_dir, "tox", "tox-pip-version")
        install_deps(venv_dir, PACKAGE_DIR)
        _run_case(venv_dir, case, env=env)
    finally:
        temp_dir.cleanup()
