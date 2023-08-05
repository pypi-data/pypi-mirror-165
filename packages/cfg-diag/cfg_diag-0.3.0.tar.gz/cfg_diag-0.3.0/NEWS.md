# Change log for cfg-diag library

## 0.3.0

- API break: the `.diag()` method now accepts a callable function that
  will only be invoked if needed; it must return the string to be output
- add the `.diag_()` method for strings that are not expensive to build
- list Python 3.11 as a supported version
- various Tox configuration and testing clean-ups:
  - use Pylint 2.14; it no longer outputs the `no-self-use` lint
  - drop the flake8 + hacking environment, it is incompatible with recent
    versions of flake8
  - use `pytest.mark.parametrize()` instead of the ddt module
  - add both lower and upper version constraints to most of the package
    dependencies in the Tox test environments
  - move the mypy configuration to the pyproject.toml file
  - use types-setuptools and drop a `type: ignore` annotation
- add a Nox definitions file

## 0.2.1

- include the .editorconfig file in the sdist tarball

## 0.2.0

- drop Python 3.6 as a supported version, add Python 3.10 instead
- reformat the source code using black 22 and 100 characters per line
- drop the useless basepython definition from the Tox test environments
- add a pytest >= 6 dependency for the mypy environment and drop the type stubs
- reflow the tox.ini file with a four-character indent
- add an EditorConfig definitions file
- add a flake8 + hacking Tox test environment

## 0.1.1

- move some tool configuration options to setup.py and pyproject.toml
- add Python 3.9 as a supported version
- use unittest.mock instead of mock
- fix a code comment
- add a manifest to include more files in the source distribution

## 0.1.0

- first public release
