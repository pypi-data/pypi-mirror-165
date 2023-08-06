# -*- coding: utf-8 -*-

"""

dryjq.__main__

dryjq (or python3 -m dryjq) command line script

Copyright (C) 2022 Rainer Schwarzbach

This file is part of dryjq.

dryjq is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

dryjq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import logging
import sys

from typing import List, Optional

from dryjq import commandline
from dryjq import commons
from dryjq import queries


#
# Functions
#


def main(args: Optional[List[str]] = None) -> int:
    """Use the query parser to construct
    an access.Path subclass instance from the original query.
    Then, execute the program using that instance together with
    the provided command line arguments.

    :param args: the list of command line arguments,
        or None to go with the default (sys.argv).
    :returns: the script returncode
    """
    program = commandline.Program(args)
    try:
        data_path = queries.Parser().parse_query(
            program.arguments.query,
            separator_codepoint=ord(program.arguments.separator),
            subscript_indicators_pair=commons.CharactersPair(
                program.arguments.subscript_indicators
            ),
        )
    except (
        queries.MalformedQueryError,
        queries.IllegalStateError,
        ValueError,
    ) as error:
        logging.error(error)
        return commandline.RETURNCODE_ERROR
    #
    return program.execute(data_path=data_path)


if __name__ == "__main__":
    sys.exit(main())


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
