# -*- coding: utf-8 -*-

"""

dryjq.commandline

Command line functionality

Copyright (C) 2022 Rainer Schwarzbach

This file is part of dryjq.

dryjq is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

dryjq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import argparse
import io
import logging

import sys

from typing import Dict, List, Optional, TextIO, Type

import yaml

import dryjq

from dryjq import access
from dryjq import commons
from dryjq import streams


#
# Constants
#


RETURNCODE_OK = 0
RETURNCODE_ERROR = 1


#
# classes
#


class Program:

    """Command line program"""

    name: str = "dryjq"
    description: str = "Drastically Reduced YAML / JSON Query"
    query_option: bool = True
    modify_in_place_option: bool = True
    default_output_format: str = commons.FORMAT_INPUT

    allowed_formats: Dict[str, str] = {
        commons.FORMAT_JSON: "set output format to JSON",
        commons.FORMAT_YAML: "set output fromat to YAML",
        commons.FORMAT_INPUT: "keep input format",
        commons.FORMAT_TOGGLE: "change JSON to YAML or vice versa",
    }

    def __init__(self, args: Optional[List[str]] = None) -> None:
        """Parse command line arguments and initialize the logger

        :param args: a list of command line arguments
        """
        self.__arguments = self._parse_args(args)
        if self.__arguments.loglevel < logging.INFO:
            message_format = (
                "%(levelname)-8s | (%(funcName)s:%(lineno)s) %(message)s"
            )
        else:
            message_format = "%(levelname)-8s | %(message)s"
        #
        if self.query_option and self.__arguments.query is None:
            self.__arguments.query = self.__arguments.separator
        #
        logging.basicConfig(
            format=message_format,
            level=self.__arguments.loglevel,
        )

    @property
    def arguments(self) -> argparse.Namespace:
        """Property: command line arguments

        :returns: the parsed command line arguments
        """
        return self.__arguments

    @classmethod
    def complete_format(cls, input_format: str) -> str:
        """Lookup the matching format

        :param input_format: the (case insensitive) start of
            any allowed input format
        :returns: the matching format
        :raises: ValueError if the no matching format was found
        """
        lower_input_format = input_format.lower()
        for candidate in cls.allowed_formats:
            if candidate.lower().startswith(lower_input_format):
                return candidate
            #
        #
        raise ValueError(f"Unsupported format {input_format!r}!")

    def _parse_args(self, args: Optional[List[str]]) -> argparse.Namespace:
        """Parse command line arguments using argparse
        and return the arguments namespace.

        :param args: a list of command line arguments,
            or None to parse sys.argv
        :returns: the parsed command line arguments as returned
            by argparse.ArgumentParser().parse_args()
        """
        main_parser = argparse.ArgumentParser(
            prog=self.name,
            description=self.description,
        )
        main_parser.set_defaults(
            loglevel=logging.WARNING,
            output_format=self.default_output_format,
            indent=commons.DEFAULT_INDENT,
            inplace=False,
            separator=commons.DEFAULT_SEPARATOR,
            subscript_indicators=commons.DEFAULT_SUBSCRIPT_INDICATORS,
        )
        main_parser.add_argument(
            "--version",
            action="version",
            version=f"%(prog)s {dryjq.__version__}",
            help="print version and exit",
        )
        if self.modify_in_place_option:
            main_parser.add_argument(
                "-i",
                "--inplace",
                action="store_true",
                help="modify the input file in place instead of writing"
                " the result to standard output",
            )
        #
        logging_group = main_parser.add_argument_group(
            "Logging options", "control log level (default is WARNING)"
        )
        verbosity = logging_group.add_mutually_exclusive_group()
        verbosity.add_argument(
            "-d",
            "--debug",
            action="store_const",
            const=logging.DEBUG,
            dest="loglevel",
            help="output all messages (log level DEBUG)",
        )
        verbosity.add_argument(
            "-v",
            "--verbose",
            action="store_const",
            const=logging.INFO,
            dest="loglevel",
            help="be more verbose (log level INFO)",
        )
        verbosity.add_argument(
            "-q",
            "--quiet",
            action="store_const",
            const=logging.ERROR,
            dest="loglevel",
            help="be more quiet (log level ERROR)",
        )
        output_group = main_parser.add_argument_group(
            "Output options", "control output formatting"
        )
        format_choices = ", ".join(
            f"{key!r}: {value}"
            for (key, value) in self.allowed_formats.items()
        )
        output_group.add_argument(
            "-o",
            "--output-format",
            type=self.complete_format,
            help=f"output format (choice of {format_choices};"
            " default: %(default)r)",
        )
        output_group.add_argument(
            "--indent",
            choices=(2, 4, 8),
            type=int,
            help="indentation depth of blocks, in spaces"
            " (default: %(default)s)",
        )
        output_group.add_argument(
            "--sort-keys",
            action="store_true",
            help="sort mapping keys"
            " (by default, mapping keys are left in input order)",
        )
        if self.query_option:
            query_syntax_group = main_parser.add_argument_group(
                "Query syntax options", "control the query syntax"
            )
            query_syntax_group.add_argument(
                "--separator",
                help="the separator character (default: %(default)r)",
            )
            query_syntax_group.add_argument(
                "--subscript-indicators",
                help="the subscript indicator character(s)"
                " (default: %(default)r)",
            )
            main_parser.add_argument(
                "query",
                nargs="?",
                help="the query (simplest form of yq/jq syntax,"
                " default is the separator character alone).",
            )
        #
        main_parser.add_argument(
            "input_file",
            nargs="?",
            help="the input file name"
            " (by default, data will be read from standard input)",
        )
        return main_parser.parse_args(args)

    def _write_filtered_data(
        self,
        handler_class: Type[streams.StreamReader],
        stream: TextIO,
        data_path: Optional[access.Path] = None,
    ) -> int:
        """Execute the query using the data path,
        write output and return the returncode.
        Catch all expected exceptions and log them using ERROR loglevel.

        :param handler_class: a streams.StreamReader
            (or subclass) instance
        :param stream: the (text) IO stream containing the
            serialized data structure
        :param data_path: the access.Path subclass constructed
            from the original query
        :returns: the returncode for the script
        """
        try:
            stream_handler = handler_class(stream)
        except (yaml.YAMLError, yaml.composer.ComposerError) as error:
            for line in str(error).splitlines():
                logging.error(line)
            #
            return RETURNCODE_ERROR
        #
        try:
            if data_path is None:
                logging.debug("Skipping empty query")
            else:
                stream_handler.execute_single_query(data_path)
            #
            stream_handler.set_serialization_format(
                output_format=self.arguments.output_format,
                indent=self.arguments.indent,
                sort_keys=self.arguments.sort_keys,
            )
            stream_handler.write_output()
        except (TypeError, ValueError, yaml.YAMLError) as error:
            for line in str(error).splitlines():
                logging.error(line)
            #
            return RETURNCODE_ERROR
        #
        return RETURNCODE_OK

    def execute(
        self,
        data_path: Optional[access.Path] = None,
    ) -> int:
        """Execute the program

        :param data_path: the access.Path subclass constructed
            from the original query
        :returns: the returncode for the script
        """
        display_mode = "extract mode"
        replace_mode = isinstance(data_path, access.ReplacingPath)
        if replace_mode:
            display_mode = "replace mode"
        elif not data_path:
            display_mode = f"{display_mode} (passthrough)"
        #
        stream_handler_class = streams.StreamReader
        logging.info("Operating in %s.", display_mode)
        if self.arguments.input_file is None:
            if self.arguments.inplace:
                logging.warning("Cannot modify <stdin> in place")
            #
            logging.info("- ↓↓↓ Reading data from standard input")
            return self._write_filtered_data(
                stream_handler_class,
                sys.stdin,
                data_path=data_path,
            )
        #
        file_open_mode = "r"
        if replace_mode and self.arguments.inplace:
            file_open_mode = "r+"
            stream_handler_class = streams.FileWriter
        #
        with open(
            self.arguments.input_file,
            mode=file_open_mode,
            encoding="utf-8",
        ) as input_file:
            logging.info(
                "----- Reading data from file: %s", self.arguments.input_file
            )
            # Help mypy to be strict about the file type (TextIO)
            if isinstance(input_file, io.TextIOBase):
                returncode = self._write_filtered_data(
                    stream_handler_class,
                    input_file,
                    data_path,
                )
            else:
                logging.error("Not a text file!")
                return RETURNCODE_ERROR
            #
        #
        return returncode


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
