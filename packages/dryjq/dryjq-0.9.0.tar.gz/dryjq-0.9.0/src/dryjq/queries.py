# -*- coding: utf-8 -*-

"""

dryjq.queries

Query parser and helper classes

Copyright (C) 2022 Rainer Schwarzbach

This file is part of dryjq.

dryjq is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

dryjq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import collections
import dataclasses
import logging

from typing import Iterator, List, Optional, Type

import yaml

from dryjq import access
from dryjq import commons


#
# Item dataclasses
#


@dataclasses.dataclass(frozen=True)
class BaseItem:

    """Base class for all items"""


@dataclasses.dataclass(frozen=True)
class DelimiterItem(BaseItem):

    """Start or end item"""

    end: bool = False


@dataclasses.dataclass(frozen=True)
class ItemWithContent(BaseItem):

    """Base class for items with content"""

    content: str


@dataclasses.dataclass(frozen=True)
class AssignmentItem(ItemWithContent):

    """Assignment item"""


@dataclasses.dataclass(frozen=True)
class LiteralItem(ItemWithContent):

    """Literal item"""


@dataclasses.dataclass(frozen=True)
class SeparatorItem(ItemWithContent):

    """Separator item"""


@dataclasses.dataclass(frozen=True)
class SubscriptOpenerItem(ItemWithContent):

    """Subscript opener item"""


@dataclasses.dataclass(frozen=True)
class SubscriptCloserItem(ItemWithContent):

    """Subscript closer item"""


@dataclasses.dataclass(frozen=True)
class WhitespaceItem(ItemWithContent):

    """Whitespace item"""


#
# Exceptions
#


class IllegalStateError(Exception):

    """Exception raised if the parser is in an illegal state"""

    def __init__(
        self,
        message: str,
        offending_item: BaseItem,
        parser_phase: Optional[str] = None,
        position: int = 0,
    ) -> None:
        """Store the message, offending item, parser state and position

        :param message: the error details
        :param offending_item: the offending item
        :param parser_phase: the current parser phase
        :param position: the offending item’s position
        """
        super().__init__()
        self.message = message
        self.offending_item = offending_item
        self.parser_phase = parser_phase
        self.position = position

    def __str__(self) -> str:
        """String representation: str()

        :returns: the full error message
        """
        position_display = ""
        if self.position:
            position_display = (
                f" at item position #{self.position}, counting from 1"
            )
            if logging.getLogger().getEffectiveLevel() > logging.DEBUG:
                position_display = (
                    f"{position_display}; enable debug mode (-d)"
                    " for a list of determined items and their positions"
                )
            #
        #
        message = ""
        if self.message:
            message = f"\n{self.message}!"
        #
        return (
            f"Illegal state encountered{position_display}."
            f" Parser phase: {self.parser_phase!r}."
            f" Offending item: {self.offending_item!r}.{message}"
        )


class MalformedQueryError(Exception):

    """Exception raised by the itemizer on malformed queries"""

    error_type = "Malformed query"

    def __init__(self, character_position: int = 0) -> None:
        """Store the character position

        :param character_position: the character position
            which is significant for the error
        """
        super().__init__()
        self.character_position = character_position

    def __str__(self) -> str:
        """String representation: str()

        :returns: the full error message
        """
        return (
            f"{self.error_type} at character position"
            f" #{self.character_position} (counting from 1)"
        )


class UnclosedQuoteError(MalformedQueryError):

    """Exception raised when a quote was not closed"""

    error_type = "Unclosed quote started"


class UnclosedSubscriptError(MalformedQueryError):

    """Exception raised when a subscript was not closed"""

    error_type = "Unclosed subscript started"


#
# Classes
#


class Itemizer:

    """Itemize a query string for the parser"""

    quotes = (0x22, 0x27)
    equals_sign = 0x3D
    whitespace = (0x09, 0x0A, 0x0D, 0x20)

    def __init__(
        self,
        separator_codepoint: Optional[int] = None,
        subscript_indicators_pair: Optional[commons.CharactersPair] = None,
    ) -> None:
        """Initialize the itemizer internal state

        :param separator_codepoint: (optionally) the codepoint
            of the separator
        :param subscript_indicators_pair: (optionally) the subscript
            indicators pair
        :raises: ValueError if the separator codepoint or any of the
            subscript indicator codepoints are already taken,
            see the quotes, equals_sign and whitespace definitions
            in the class.
        """
        reserved_codepoints: set[int] = {
            self.equals_sign,
            *self.quotes,
            *self.whitespace,
        }
        if subscript_indicators_pair is None:
            subscript_indicators_pair = commons.CharactersPair(
                commons.DEFAULT_SUBSCRIPT_INDICATORS
            )
        #
        for subscript_codepoint in subscript_indicators_pair.both:
            if subscript_codepoint in reserved_codepoints:
                raise ValueError(
                    f"Subscript indicator codepoint {subscript_codepoint}"
                    f" ({chr(subscript_codepoint)!r}) not allowed,"
                    f" must not be any of {reserved_codepoints}!"
                )
            #
        #
        reserved_codepoints.update(subscript_indicators_pair.both)
        if separator_codepoint is None:
            separator_codepoint = ord(commons.DEFAULT_SEPARATOR)
        #
        if separator_codepoint in reserved_codepoints:
            raise ValueError(
                f"Separator codepoint {separator_codepoint}"
                f" ({chr(separator_codepoint)!r}) not allowed,"
                f" must not be any of {reserved_codepoints}!"
            )
        #
        self.__character_position = 0
        self.__current_literal: List[str] = []
        self.__items_queue: collections.deque[BaseItem] = collections.deque()
        self.__query_characters: collections.deque[str] = collections.deque()
        self.__separator_codepoint = separator_codepoint
        self.__subscript_indicators_pair = subscript_indicators_pair
        self.__subscript_start_position = 0

    @property
    def separator_codepoint(self) -> int:
        """Property: separator codepoint

        :returns: the separator codepoint
        """
        return self.__separator_codepoint

    @property
    def subscript_indicators_pair(self) -> commons.CharactersPair:
        """Property: subscript indicators

        :returns: the subscript indicators characters pair
        """
        return self.__subscript_indicators_pair

    def _add_current_literal(self) -> None:
        """Add a new LiteralItem from the current literal
        if any literal fragments have been collected yet.
        """
        if self.__current_literal:
            self.__items_queue.append(
                LiteralItem("".join(self.__current_literal))
            )
            self.__current_literal.clear()
        #

    def _append_literal_codepoint(self, codepoint: int) -> None:
        """Append the codepoint character to the current literal

        :param codepoint: the codepoint of the character to append
        """
        self.__current_literal.append(chr(codepoint))

    def _feed_characters(self) -> None:
        """Internal dispatcher method
        calling the appropriate processing methods
        """
        codepoint = self._pop_next_codepoint()
        if codepoint in self.quotes:
            self._process_quoted(codepoint)
        elif self.__subscript_start_position:
            self._process_in_subscript(codepoint)
        else:
            self._process_normal(codepoint)
        #

    def _pop_next_codepoint(self) -> int:
        """Pop the next character from the queue
        and increment the character position.

        :returns: the codepoint of the character
        """
        character = self.__query_characters.popleft()
        self.__character_position += 1
        return ord(character)

    def _process_quoted(self, quote_codepoint: int) -> None:
        """Process an opening quote and everything
        up to and including the expected closing quote.

        :param quote_codepoint: the quote codepoint to process
        :raises: UnclosedQouteException if the end of the
            query was encountered
        """
        self._add_current_literal()
        quote_started_at = self.__character_position
        expected_closing_quote = quote_codepoint
        self._append_literal_codepoint(quote_codepoint)
        while True:
            try:
                codepoint = self._pop_next_codepoint()
            except IndexError as error:
                raise UnclosedQuoteError(
                    character_position=quote_started_at
                ) from error
            #
            self._append_literal_codepoint(codepoint)
            if codepoint == expected_closing_quote:
                break
            #
        #
        self._add_current_literal()

    def _process_in_subscript(self, codepoint: int) -> None:
        """Process characters in subscript,
        treating equal signs and separators as literal components.

        :param codepoint: the codepoint to process
        """
        if codepoint in (
            self.subscript_indicators_pair.close,
            *self.whitespace,
        ):
            self._add_current_literal()
            item_constructor: Type[ItemWithContent]
            if codepoint == self.subscript_indicators_pair.close:
                self.__subscript_start_position = 0
                item_constructor = SubscriptCloserItem
            else:
                item_constructor = WhitespaceItem
            #
            self.__items_queue.append(item_constructor(chr(codepoint)))
        else:
            self._append_literal_codepoint(codepoint)
            if codepoint == self.subscript_indicators_pair.open:
                logging.warning(
                    "Possible error: Found subscript opener character %s (%r)"
                    " at position #%r inside a subscript",
                    hex(codepoint),
                    chr(codepoint),
                    self.__character_position,
                )
            #
        #

    def _process_normal(self, codepoint: int) -> None:
        """Normal processing of a single character from the query:
        opening subscript indicator, equals sign, separator,
        whitespace or literal content

        :param codepoint: the codepoint to process
        """
        if codepoint in (
            self.subscript_indicators_pair.open,
            self.separator_codepoint,
            self.equals_sign,
            *self.whitespace,
        ):
            self._add_current_literal()
            item_constructor: Type[ItemWithContent]
            if codepoint == self.subscript_indicators_pair.open:
                item_constructor = SubscriptOpenerItem
                self.__subscript_start_position = self.__character_position
            elif codepoint == self.equals_sign:
                item_constructor = AssignmentItem
            elif codepoint == self.separator_codepoint:
                item_constructor = SeparatorItem
            else:
                # implicit "codepoint in self.whitespace"
                item_constructor = WhitespaceItem
            #
            self.__items_queue.append(item_constructor(chr(codepoint)))
        else:
            self._append_literal_codepoint(codepoint)
        #

    def _reset(self) -> None:
        """Reset the itemizer"""
        self.__character_position = 0
        self.__current_literal.clear()
        self.__items_queue.clear()
        self.__query_characters.clear()
        self.__subscript_start_position = 0

    def itemize(self, original_query: str) -> Iterator[BaseItem]:
        """Yield items from a given query string

        :param original_query: a query string to be itemized
        """
        self._reset()
        self.__query_characters.extend(original_query)
        yield DelimiterItem()
        while self.__query_characters:
            self._feed_characters()
            while self.__items_queue:
                yield self.__items_queue.popleft()
            #
        #
        if self.__subscript_start_position:
            raise UnclosedSubscriptError(
                character_position=self.__subscript_start_position
            )
        #
        self._add_current_literal()
        while self.__items_queue:
            yield self.__items_queue.popleft()
        #
        yield DelimiterItem(end=True)


class Parser:

    """Query parser"""

    phase_before_start = "before start"
    phase_started = "started"
    phase_address = "address"
    phase_replacement = "replacement"
    phase_ended = "ended"

    def __init__(self) -> None:
        """Initialize the itemizer internal state"""
        self.__in_subscript = False
        self.__phase = self.phase_before_start
        self.__collected_literals: List[LiteralItem] = []
        self.__collected_components: List[access.PathComponent] = []
        self.__replacement_fragments: List[str] = []

    @property
    def phase(self) -> str:
        """Property: current phase

        :returns: the current parser phase
        """
        return self.__phase

    def _append_path_component(self) -> None:
        """Add a path component from the collected literals

        Join adjacent literals, but yaml-safe-load them
        separately to enable mixing different quotes.
        Allow other literals than strings
        only if exactly one literal was collected.
        """
        if not self.__collected_literals:
            return
        #
        if len(self.__collected_literals) > 1:
            component_index = "".join(
                yaml.safe_load(item.content)
                for item in self.__collected_literals
            )
        else:
            component_index = yaml.safe_load(
                self.__collected_literals[0].content
            )
        #
        self.__collected_components.append(
            access.PathComponent(
                component_index, in_subscript=self.__in_subscript
            )
        )
        self.__collected_literals.clear()

    def _feed(self, item: BaseItem, position: int = 0) -> None:
        """Feed one item to the parser.
        Internal dispatcher method calling the appropriate handler
        according to the current phase.

        :param item: the item to be processed
        :param position: the item position (starting at 1)
        :raises: IllegalStateError if there is no handler defined
            for the current phase
        """
        for (phase, method) in (
            (self.phase_before_start, self._process_before_start),
            (self.phase_started, self._process_started),
            (self.phase_address, self._process_address),
            (self.phase_replacement, self._process_replacement),
            (self.phase_ended, self._process_ended),
        ):
            if phase == self.phase:
                item_handler = method
                break
            #
        else:
            raise IllegalStateError(
                "Item handler for this phase not implemented",
                offending_item=item,
                position=position,
                parser_phase=self.phase,
            )
        #
        item_handler(item, position=position)

    def _process_before_start(self, item: BaseItem, position: int = 0) -> None:
        """Process items in the "before_start" phase
        (Initial phase before processing the first item,
         which must unconditionally be a DelimiterItem).

        :param item: the item to be processed
        :param position: the item position (starting at 1)
        :raises: IllegalStateError if another item than a
            DelimiterItem(end=False) is encountered
        """
        if isinstance(item, DelimiterItem) and not item.end:
            self.__phase = self.phase_started
            return
        #
        raise IllegalStateError(
            "Expected DelimiterItem(end=False)",
            offending_item=item,
            position=position,
            parser_phase=self.phase,
        )

    def _process_started(self, item: BaseItem, position: int = 0) -> None:
        """Process items in the "started" phase
        (Phase after the start item and before the
         unconditionally required initial SeparatorItem).
        Ignore whitespace, it is allowed and ignored here.
        Switch to the next phase when the SeparatorItem was found.

        :param item: the item to be processed
        :param position: the item position (starting at 1)
        :raises: IllegalStateError if neither a WhitespaceItem
            nor a SeparatorItem is encountered
        """
        if isinstance(item, WhitespaceItem):
            return
        #
        if isinstance(item, SeparatorItem):
            self.__phase = self.phase_address
            return
        #
        raise IllegalStateError(
            "The query must always start with a separator item",
            offending_item=item,
            position=position,
            parser_phase=self.phase,
        )

    def _process_address(self, item: BaseItem, position: int = 0) -> None:
        """Process items in the "address" phase
        (Phase after the initial SeparatorItem until
         either the first AssignmentItem or the final
         DelimiterItem is encountered).
        Collect literals for the address components.
        Switch phases if one of the aforementioned items was found.

        :param item: the item to be processed
        :param position: the item position (starting at 1)
        :raises: IllegalStateError if a DelimiterItem(end=False)
            is encountered
        """
        if isinstance(item, LiteralItem):
            self.__collected_literals.append(item)
            return
        #
        if isinstance(
            item,
            (
                AssignmentItem,
                DelimiterItem,
                SeparatorItem,
                SubscriptCloserItem,
                SubscriptOpenerItem,
            ),
        ):
            self._append_path_component()
        #
        if isinstance(item, AssignmentItem):
            self.__phase = self.phase_replacement
        elif isinstance(item, DelimiterItem):
            if item.end:
                self.__phase = self.phase_ended
            else:
                raise IllegalStateError(
                    "DelimiterItem(end=False) not allowed here",
                    offending_item=item,
                    position=position,
                    parser_phase=self.phase,
                )
            #
        elif isinstance(item, SubscriptOpenerItem):
            self.__in_subscript = True
        elif isinstance(item, SubscriptCloserItem):
            self.__in_subscript = False
        #

    def _process_replacement(self, item: BaseItem, position: int = 0) -> None:
        """Process items in the "replacement" phase
        (Phase after the first AssignmentItem is encountered).
        Collect all Items having content for the replacement components.
        Switch phases if a DelimiterItem was found.

        :param item: the item to be processed
        :param position: the item position (starting at 1)
        :raises: IllegalStateError if a DelimiterItem(end=False)
            is encountered
        """
        if isinstance(item, DelimiterItem):
            if item.end:
                if not self.__replacement_fragments:
                    self.__replacement_fragments.append("")
                #
                self.__phase = self.phase_ended
            else:
                raise IllegalStateError(
                    "DelimiterItem(end=False) not allowed here",
                    offending_item=item,
                    position=position,
                    parser_phase=self.phase,
                )
            #
        elif isinstance(item, ItemWithContent):
            self.__replacement_fragments.append(item.content)
        #

    def _process_ended(self, item: BaseItem, position: int = 0) -> None:
        """Process items in the "ended" phase
        (Phase after the final DelimiterItem is encountered).
        No items allowed anymore in this phase.

        :param item: the item to be processed
        :param position: the item position (starting at 1)
        :raises: IllegalStateError unconditionally
        """
        raise IllegalStateError(
            "No items allowed anymore",
            offending_item=item,
            position=position,
            parser_phase=self.phase,
        )

    def _reset(self) -> None:
        """Reset the parser"""
        self.__in_subscript = False
        self.__phase = self.phase_before_start
        self.__collected_literals.clear()
        self.__collected_components.clear()
        self.__replacement_fragments.clear()

    def parse_query(
        self,
        original_query: str,
        separator_codepoint: Optional[int] = None,
        subscript_indicators_pair: Optional[commons.CharactersPair] = None,
    ) -> access.Path:
        """Parse the given query and return a data structure address
        (access.ExtractingPath or access.ReplacingPath)

        :param original_query: a query string to be parsed
        :param separator_codepoint: (optionally) the codepoint
            of the separator
        :param subscript_indicators_pair: (optionally) the subscript
            indicators pair
        :returns: an access.Path subclass instance determined
            from the query string
        """
        self._reset()
        itemizer = Itemizer(
            separator_codepoint=separator_codepoint,
            subscript_indicators_pair=subscript_indicators_pair,
        )
        logging.debug("Found items in query:")
        for index, item in enumerate(itemizer.itemize(original_query)):
            position = index + 1
            logging.debug("%4d) %r", position, item)
            self._feed(item, position=position)
        #
        logging.debug("Path components: %r", self.__collected_components)
        if not self.__replacement_fragments:
            return access.ExtractingPath(*self.__collected_components)
        #
        logging.debug(
            "Replacement fragments: %r",
            self.__replacement_fragments,
        )
        serialized_replacement = "".join(self.__replacement_fragments).strip()
        if not serialized_replacement:
            logging.warning("Assuming empty assignment value -> None")
        #
        replacement_value = yaml.safe_load(serialized_replacement)
        logging.debug("Replacement value: %r", replacement_value)
        return access.ReplacingPath(
            *self.__collected_components, replacement=replacement_value
        )


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
