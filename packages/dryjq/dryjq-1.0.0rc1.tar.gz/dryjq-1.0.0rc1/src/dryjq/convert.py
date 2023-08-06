# -*- coding: utf-8 -*-

"""

dryjq.convert

dryjq.convert (or python3 -m dryjq.convert) command line script

Copyright (C) 2022 Rainer Schwarzbach

This file is part of dryjq.

dryjq is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

dryjq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import sys

from typing import List, Optional

from dryjq import commons
from dryjq import commandline


#
# Classes
#


class ConvertProgram(commandline.Program):

    """Conversion program
    commandline.Program subclass with less command line arguments
    and a different default output format compared to the parent class
    """

    name: str = "dryjq.convert"
    description: str = "Drastically Reduced YAML / JSON Query: convert files"
    query_option: bool = False
    modify_in_place_option: bool = False
    default_output_format: str = commons.FORMAT_TOGGLE


#
# Functions
#


def main(args: Optional[List[str]] = None) -> int:
    """Execute the program using the provided command line arguments

    :param args: the list of command line arguments,
        or None to go with the default (sys.argv).
    :returns: the script returncode
    """
    program = ConvertProgram(args)
    return program.execute()


if __name__ == "__main__":
    sys.exit(main())


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
