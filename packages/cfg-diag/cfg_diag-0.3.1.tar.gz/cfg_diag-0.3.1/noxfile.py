#
# Copyright (c) 2022  StorPool
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
"""Test definitions for the Nox test runner."""

import pathlib
import tempfile

import nox


nox.needs_version = ">= 2022.8.7"

PYFILES = [
    "noxfile.py",
    "src/cfg_diag",
    "setup.py",
    "unit_tests",
]

DEPS = {
    "black": ["black >= 22, < 23"],
    "pytest": ["pytest >= 7, < 8"],
    "test": ["pytest >= 7, < 8"],
}


@nox.session(name="black-reformat")
def black_reformat(session: nox.Session) -> None:
    """Reformat the source files using the black tool."""
    if session.posargs != ["do", "reformat"]:
        raise Exception("The black-reformat session is special")

    session.install(*DEPS["black"])
    session.run("black", *PYFILES)


@nox.session(tags=["check"])
def black(session: nox.Session) -> None:
    """Run the black format checker on the source files."""
    session.install(*DEPS["black"])
    session.run("black", "--check", *PYFILES)


@nox.session(tags=["check"])
def pep8(session: nox.Session) -> None:
    """Run the flake8 checker on the source files."""
    session.install("flake8 >= 5, < 6")
    session.run("flake8", *PYFILES)


@nox.session(tags=["check"])
def mypy(session: nox.Session) -> None:
    """Run the mypy type checker on the source files."""
    session.install("mypy >= 0.942", "nox >= 2022.8.7", "types-setuptools", *DEPS["pytest"])
    session.run("mypy", *PYFILES)


@nox.session(tags=["check"])
def pylint(session: nox.Session) -> None:
    """Run the pylint checker on the source files."""
    session.install("nox >= 2022.8.7", "pylint >= 2.14, < 2.16", *DEPS["pytest"])
    session.run("pylint", *PYFILES)


@nox.session(tags=["tests"])
def unit_tests(session: nox.Session) -> None:
    """Build a wheel, run the unit test suite using pytest."""
    with tempfile.TemporaryDirectory() as tempd_obj:
        tempd = pathlib.Path(tempd_obj)
        print(f"Using {tempd} as a temporary directory")

        session.install("build")
        session.run("python3", "-m", "build", "--wheel", "--outdir", str(tempd))
        files = [item for item in tempd.iterdir() if item.is_file()]
        if len(files) != 1:
            raise Exception(f"Unexpected number of files in {tempd}: {files!r}")
        wheel = files[0]
        if not (wheel.name.startswith("cfg_diag-") and wheel.name.endswith(".whl")):
            raise Exception(f"Unexpected built wheel filename: {wheel}")
        print(f"Found a wheel: {wheel}")

        session.install(str(wheel), *DEPS["pytest"])
        session.run("pytest", "unit_tests")
