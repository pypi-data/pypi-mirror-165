import re
from pathlib import Path
from typing import Iterator, Optional, Tuple, Union

from dotenv.main import DotEnv, find_dotenv
from dotenv.parser import parse_stream

SET_A = re.compile(r"^\s*set\s+-a\s*$")


class WDotEnv(DotEnv):
    """
    We override the default DotEnv class in order to alter error reporting.
    First of all, we want to allow `set -a` in files without getting an error.
    And then we want the option to be able to look at the list of errors and
    to report them through a different channel than the default warning from
    the lib.
    """

    def parse(self) -> Iterator[Tuple[str, Optional[str]]]:
        """
        Same as the parent but ignoring errors on `set -a`.
        """

        with self._get_stream() as stream:
            setattr(self, "_error_lines", [])

            for binding in parse_stream(stream):
                if binding.error:
                    if not SET_A.match(binding.original.string):
                        self.error_lines.append(binding.original)
                else:
                    yield binding.key, binding.value

    @property
    def error_lines(self):
        """
        A shortcut to get error lines reported during parsing
        """

        return getattr(self, "_error_lines", [])


def load_dotenv(dotenv_path: Union[str, Path, None] = None) -> bool:
    """
    Finds, parses and loads as default the .env file for this project.

    If the path is not specified, it will use find_dotenv() which looks along
    the stack trace to find the code root and find the .env file associated.

    Parameters
    ----------
    dotenv_path
        Optional path to the dotenv file, which will otherwise be guessed
    """

    if dotenv_path is None:
        dotenv_path = find_dotenv()

    dotenv = WDotEnv(dotenv_path=dotenv_path)

    return dotenv.set_as_environment_variables()
