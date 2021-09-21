# Contributing to tox-setuptools-version

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

## Code architecture

All CI/CD and manual actions could (and should) be made through tox. 

### Run tests

If you want to run the tests do 

```console
tox
```

### Black

To follow the python best practices, we use [black](https://github.com/psf/black). If you want to run this tool locally, you can do

```console
tox -e black
```
