#
# Copyright (c) 2021, 2022  StorPool
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
"""A common configuration-storage class with a .diag() method.

This module provides four classes that may be used as base classes for
storing program runtime configuration with a `verbose` boolean field.
The classes provide a `.diag(func)` method that will check the object's
`verbose` field and, if it is set to a true value, invoke the specified
function and output the message that it returns. If the message is not
expensive to format (e.g. it does not include stringifying elaborate
data structures), the `.diag(msg)` method may be used instead.

The `ConfigDiagUnfrozen` and `ConfigDiagUnfrozenStdOut` classes are
normal dataclasses, while the `ConfigDiag` and `ConfigDiagStdOut` ones
are frozen.

The `ConfigDiag` and `ConfigDiagUnfrozen` classes will output any
diagnostic messages to the standard error stream, while
the `ConfigDiagStdOut` and `ConfigDiagUnfrozenStdOut` ones will output
the diagnostic messages to the standard output stream.

Example:

Subclass the frozen `ConfigDiag` class, add a program-specific field:

    @dataclasses.dataclass(frozen=True)
    class Config(cfg_diag.ConfigDiag):
        '''Runtime configuration for the fribble program.'''
        path: pathlib.Path

Initialize this class from an argument parser object:

    return Config(path=args.path, verbose=args.verbose)

Output a diagnostic message if requested:

    cfg.diag_("This will either appear or it will not")
    cfg.diag(lambda: f"Here's the thing: {thing!r}")
"""


import dataclasses
import sys

from typing import Callable


VERSION = "0.3.1"


class ConfigDiagBase:
    """Output diagnostic messages if requested.

    Child classes MUST define a boolean-like `verbose` attribute!
    """

    # pylint: disable=too-few-public-methods

    _config_diag_to_stderr = True

    def diag(self, func: Callable[[], str]) -> None:
        """Output the diagnostic message returned by the function if requested."""
        if self.verbose:  # type: ignore  # pylint: disable=no-member
            print(
                func(),
                file=sys.stderr if self._config_diag_to_stderr else sys.stdout,
            )

    def diag_(self, msg: str) -> None:
        """Output a diagnostic message if requested."""
        self.diag(lambda: msg)


@dataclasses.dataclass
class ConfigDiagUnfrozen(ConfigDiagBase):
    """A base class for configuration storage."""

    verbose: bool


@dataclasses.dataclass(frozen=True)
class ConfigDiag(ConfigDiagBase):
    """A frozen base class for configuration storage."""

    verbose: bool


@dataclasses.dataclass
class ConfigDiagUnfrozenStdOut(ConfigDiagUnfrozen):
    """A base class that outputs diagnostic messages to stdout."""

    def __post_init__(self) -> None:
        """Redirect the output to the standard output stream."""
        self._config_diag_to_stderr = False


@dataclasses.dataclass(frozen=True)
class ConfigDiagStdOut(ConfigDiag):
    """A frozen base class with diagnostic messages output to stdout."""

    def __post_init__(self) -> None:
        """Redirect the output to the standard output stream."""
        object.__setattr__(self, "_config_diag_to_stderr", False)
