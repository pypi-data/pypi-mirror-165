# -*- coding: utf-8 -*-

"""

dryjq.commons

Common constants and helper classes

Copyright (C) 2022 Rainer Schwarzbach

This file is part of dryjq.

dryjq is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

dryjq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""

from typing import Tuple


DEFAULT_INDENT = 2
DEFAULT_SEPARATOR = "."
DEFAULT_SUBSCRIPT_INDICATORS = "[]"

FORMAT_INPUT = "input"
FORMAT_JSON = "JSON"
FORMAT_YAML = "YAML"
FORMAT_TOGGLE = "toggle"

SUPPORTED_FORMATS = (FORMAT_JSON, FORMAT_YAML)


#
# Classes
#


class CharactersPair:

    """Helper class keeping a pair of characters"""

    def __init__(self, source: str) -> None:
        """Store the codepoints of first and second character

        :param source: a string of 1 or 2 characters length
        :raises: ValueError if the string length exceeds 2,
            IndexError if an empty string was provided.
        """
        if len(source) > 2:
            raise ValueError("Please provide one or two characters only!")
        #
        self.__first_codepoint = ord(source[0])
        try:
            self.__last_codepoint = ord(source[1])
        except IndexError:
            self.__last_codepoint = self.__first_codepoint
        #
        self.__source = source

    @property
    def source(self) -> str:
        """Property: the source

        :returns: the source string
        """
        return self.__source

    @property
    def first(self) -> int:
        """Property: first codepoint

        :returns: the first codepoint
        """
        return self.__first_codepoint

    @property
    def last(self) -> int:
        """Property: last codepoint

        :returns: the last (=second) codepoint
        """
        return self.__last_codepoint

    @property
    def both(self) -> Tuple[int, int]:
        """Property: both codepoints

        :returns: a tuple containing both codepoints in order
        """
        return (self.first, self.last)

    # Aliases for the properies
    open = first
    close = last

    def __eq__(self, other):
        """Comparison: self == other
        Focus on equal effect of the instances,
        not on exact equal initialization.

        :param other: another instance of the same class
        :returns: True if the 'both' property of both instances
            are equal, False otherwise
        """
        return self.both == other.both

    def __hash__(self):
        """Hash value computation: hash()

        :returns: the hash value of the source
        """
        return hash(self.source)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
