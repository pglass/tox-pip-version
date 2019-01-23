Overview
--------

This is a tox plugin that preinstalls a specific version of pip in each tox
environment.

This works around the default behavior of tox/virtualenv that always installs
the latest version pip. It is an improvment over the `VIRTUALENV_NO_DOWNLOAD=1`
option that does not install the latest version, but could result in usage of
an outdated version of pip.

*Recommendation*: Do not pin the pip version long term. You get more stable
repeatable builds, but at the cost of using an outdated (possibly vulnerable)
package. This should be used as a temporary fix for breakages in upstream pip,
or in conjunction with a regular process to update the version pin.



### Usage

Install the package and then include `pip_version` in your tox.ini

```
[testenv]
pip_version = 19.0.1
```

This will install that specific pip into the tox-created virtualenv, before
dependencies are installed.

If the plugin is installed `pip_version` is not provided, the plugin does
nothing.
