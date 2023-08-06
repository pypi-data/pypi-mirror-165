# -*- coding: utf-8 -*-

"""

dryjq.access

Data structure access using Path objects

Copyright (C) 2022 Rainer Schwarzbach

This file is part of dryjq.

dryjq is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

dryjq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import copy
import dataclasses
import logging

from typing import Any, Tuple, Union


@dataclasses.dataclass(frozen=True)
class PathComponent:

    """single index component of a Path"""

    index: Union[str, int, float, bool, None]
    in_subscript: bool = False

    def __post_init__(self):
        """Check type of self.index

        :raises: TypeError if self.index is not
            a number, a string, a boolean or None
        """
        if not isinstance(self.index, Union[str, int, float, bool, None]):
            raise TypeError(
                "The index must be a scalar of type int, float, str, bool,"
                " or None."
            )
        #

    @property
    def allows_lists(self) -> bool:
        """Property: does this instance allow lists?
        Depends on the type of the index and the in_subscript attribute

        :returns: True if the instance allows lists, False otherwise
        """
        return self.in_subscript and isinstance(self.index, int)

    def get_value(self, data_structure: Any) -> Any:
        """Get the value or substructure determined by self.index
        from the provided data structure

        :param data_structure: a data structure to get the value from
        :returns: the resulting value or data substructure
        :raises: TypeError on incompatible types,
            or ValueError if the index was not found in the data structure
        """
        if isinstance(data_structure, list):
            if isinstance(self.index, int):
                if self.in_subscript:
                    try:
                        return data_structure[self.index]
                    except IndexError as error:
                        if data_structure:
                            logging.info(
                                "Index %r is not in allowed range (%r..%r)",
                                self.index,
                                -len(data_structure),
                                len(data_structure) - 1,
                            )
                        else:
                            logging.info(
                                "Index %r is not suitable for an empty list",
                                self.index,
                            )
                        #
                        raise ValueError(
                            f"Index {self.index!r} not found!"
                        ) from error
                    #
                #
            #
            if self.in_subscript:
                reason = "not a valid list index"
            else:
                reason = "not in subscript"
            #
            logging.info(
                "Index %r is not suitable for lists (%r)",
                self.index,
                reason,
            )
            raise TypeError(f"{self!r} does not allow lists!")
        #
        if isinstance(data_structure, dict):
            try:
                return data_structure[self.index]
            except KeyError as error:
                logging.info(
                    "Index (key) %r not found in %r",
                    self.index,
                    list(data_structure),
                )
                raise ValueError(f"Index {self.index!r} not found!") from error
            #
        #
        # raise TypeError data_structure is a scalar value
        logging.info(
            "Index %r is not suitable for %r",
            self.index,
            data_structure,
        )
        raise TypeError(
            f"Scalar value {data_structure!r} cannot have an index!"
        )

    def __str__(self) -> str:
        """Return a verbose representation: str()

        :returns: a string representation
        """
        if self.allows_lists:
            purpose = "for maps and lists"
        else:
            purpose = "for maps only"
        #
        return f"<Index {self.index!r} ({purpose})>"


class Path:

    """Address in data structures,
    an immutable sequence of PathComponent instances.
    """

    def __init__(self, *components: PathComponent) -> None:
        """Initialize the internal components

        :param components: an arbitrary number of PathComponent instances
            as positional arguments
        """
        self.__components = components

    @property
    def components(self) -> Tuple[PathComponent, ...]:
        """Property: the path components

        :returns: the components in a tuple
        """
        return self.__components

    def apply_to(self, data_structure: Any) -> Any:
        """Abstract method: apply the path to the datastructure
        and return the result, see implementations in subclasses

        :param data_structure: a data structure to operate on
        :returns: subclasses return the result
        :raises: NotImplementedError (being an abstract method)
        """
        raise NotImplementedError

    def __eq__(self, other) -> bool:
        """Comparison: self == other
        Components must be the same in both instances

        :param other: another instance of the same class
        :returns: True if the components of both instances
            are equal, False otherwise
        """
        if self.__class__ != other.__class__:
            raise TypeError(
                f"Cannot compare {self.__class__} and"
                f" {other.__class__} instances!"
            )
        #
        return self.components == other.components

    def __hash__(self) -> int:
        """Hash value computation: hash()

        :returns: the hash value of the components tuple
        """
        return hash(self.components)

    def __len__(self) -> int:
        """Length comuptation: len()

        :returns: the number of components
        """
        return len(self.components)

    def __repr__(self) -> str:
        """String representation: repr()

        :returns: a string representation
        """
        return f"{self.__class__.__name__}{self.components}"


class ExtractingPath(Path):

    """Path subclass for extracting values"""

    def apply_to(self, data_structure: Any) -> Any:
        """Get a value or substructure from the provided data structure

        :param data_structure: a data structure to get the value from
        :returns: the result value or data substructure
        :raises: TypeError on incompatible types,
            or ValueError if the index was not found in the data structure
            (summarizing KeyError on dicts and IndexError on lists)
            - re-raised from any involved PathComponent instance -
        """
        current_value = data_structure
        for element in self.components:
            current_value = element.get_value(current_value)
        #
        return current_value


class ReplacingPath(Path):

    """Path subclass for replacing subtrees"""

    def __init__(
        self, *components: PathComponent, replacement: Any = None
    ) -> None:
        """Initialize the internal components

        :param components: an arbitrary number of PathComponent instances
            as positional arguments
        :param replacement: the replacement value
            (a scalar value or data structure)
        """
        super().__init__(*components)
        self.__replacement = replacement

    @property
    def replacement(self) -> Any:
        """Property: the replacement

        :returns: the replacement
        """
        return self.__replacement

    def __eq__(self, other) -> bool:
        """Comparison: self == other
        Components and replacement must be the same in both instances.

        :param other: another instance of the same class
        :returns: True if components and replacement
            of both instances are equal, False otherwise.
        """
        return super().__eq__(other) and self.replacement == other.replacement

    def __hash__(self) -> int:
        """Hash value computation: hash()

        :returns: the hash value of a tuple containing the components
            and a representation of the replacement
        """
        return hash((self.components, repr(self.replacement)))

    def __repr__(self) -> str:
        """String representation: repr()

        :returns: a string representation
        """
        attributes_display = [repr(component) for component in self.components]
        attributes_display.append(f"replacement={self.replacement!r}")
        return f"{self.__class__.__name__}({', '.join(attributes_display)})"

    def apply_to(self, data_structure: Any) -> Any:
        """Replace a value in a deep copy of the data structure

        :param data_structure: a data structure to operate on
        :returns: a copy of the data structure where the addressed
            datum has been replaced as determined by self.replacement
        :raises: TypeError on incompatible types,
            or ValueError if the index was not found in the data structure
            (summarizing KeyError on dicts and IndexError on lists)
            - re-raised from any involved PathComponent instance -
        """
        if not self.components:
            return self.replacement
        #
        ds_copy = copy.deepcopy(data_structure)
        current_value = ds_copy
        for element in self.components[:-1]:
            current_value = element.get_value(current_value)
        #
        last_element = self.components[-1]
        # Ensure the index to be replaced
        # aready exists in the data structure
        last_element.get_value(current_value)
        current_value[last_element.index] = self.replacement
        return ds_copy


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
