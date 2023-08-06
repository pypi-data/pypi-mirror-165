# Copyright 2021 Open Logistics Foundation
#
# Licensed under the Open Logistics License 1.0.
# For details on the licensing terms, see the LICENSE file.

"""
Definition of the BaseConfigClass that should be used as superclass for any configuration
class that should be built with the ConfigBuilder.
"""
from __future__ import annotations

import copy
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, cast

from related import TypedSequence

from config_builder.replacement_map import (
    get_current_replacement_map,
    set_replacement_map_value,
)
from config_builder.utils import check_list_type, replace_directory_in_path

logger = logging.getLogger(__name__)


@dataclass
class BaseConfigClass:
    """
    Superclass for any configuration class that should be built with the ConfigBuilder.
    """

    # During the build, the config-builder searches in the class-tree
    # for attributes which math a key of the given string_replacement_map.
    # When an attribute is found which matches the name of a key, the value of this attribute
    # is put under the according key in the string_replacement_map.
    # The key-value pairs can be used in the configuration files to define string PLACEHOLDER,
    # which are replaced at runtime.
    #
    # string_replacement_map FORMAT:
    #
    # KEY = name of the Attribute
    # VALUE = "" => has to be an empty. It will be filled at runtime
    #
    # Example:
    #
    # string_replacement_map = {
    #   ATTRIBUTE_1: ""
    # }
    #
    string_replacement_map: Dict[str, str] = field(default_factory=lambda: {})

    # mutual_attribute_map FORMAT:
    # CLASS_NAME = class name for which to define mutual exclusive parameters
    # VALUE = list of names of the attributes as strings
    #
    # Example:
    # mutual_attribute_map = {
    #     CLASS_NAME: ["ATTRIBUTE_1", "ATTRIBUTE_2"]
    # }
    mutual_attribute_map: Dict[str, List[str]] = field(default_factory=lambda: {})

    def recursive_string_replacement(
        self, string_replacement_map: Optional[Dict[str, str]] = None
    ) -> None:
        """
        Recursively scans the class-tree for string attributes (including attributes in lists
        and dictionaries) and replaces any occurrence of the keys from the global replacement map
        by the according values.

        Args:
            string_replacement_map: (Optional) An extra string_replacement_map that should be used
                                    to update the global replacement map

        Returns:
            None
        """

        if string_replacement_map is not None:
            for key, value in string_replacement_map.items():
                set_replacement_map_value(key=key, value=value)

        class_attributes = vars(self)

        for class_name, class_attribute in class_attributes.items():
            if class_attribute is not None:

                if isinstance(class_attribute, str):
                    self._replace_string_in_attribute(
                        class_name=class_name,
                    )

                # Check if object is of type List[str]
                elif isinstance(class_attribute, TypedSequence) and check_list_type(
                    obj=cast(List[str], class_attribute), obj_type=str
                ):
                    self._replace_strings_in_attribute_list(
                        class_name=class_name,
                        class_attribute=cast(List[str], class_attribute),
                    )

                elif isinstance(class_attribute, dict):
                    self._replace_strings_in_attribute_dict(
                        class_name=class_name,
                        class_attribute=class_attribute,
                    )

                elif isinstance(class_attribute, TypedSequence):
                    for seq_item in class_attribute:
                        if isinstance(seq_item, BaseConfigClass):
                            seq_item.recursive_string_replacement()

                elif isinstance(class_attribute, BaseConfigClass):
                    class_attribute.recursive_string_replacement()

    def _replace_string_in_attribute(
        self,
        class_name: str,
    ) -> None:
        """
        Check if any key of the global replacement map is contained in the class-name or
        class-attribute. If so, update it accordingly.

        Args:
            class_name: Name of the config attribute

        Returns:
            None
        """

        for key, value in get_current_replacement_map().items():
            # Don't run replacements with empty string
            if value == "":
                continue

            # Update the corresponding class_name when it is part of
            # the string_replacement_map
            if key == class_name and self.__dict__[class_name] != value:
                logger.debug(
                    f"Set attribute value of '{class_name}' "
                    f"from '{self.__dict__[class_name]}' "
                    f"to '{value}'"
                )
                self.__dict__[class_name] = value

            # Replace the occurrence of the value in the class attribute, if it is
            # a directory
            if key in self.__dict__[class_name]:
                logger.debug(
                    f"Replace '{key}' "
                    f"in value '{self.__dict__[class_name]}' "
                    f"of attribute {class_name} "
                    f"with '{value}'"
                )
                self.__dict__[class_name] = replace_directory_in_path(
                    file_path=self.__dict__[class_name],
                    replacement_key=key,
                    replacement_value=value,
                )

    def _replace_strings_in_attribute_list(
        self,
        class_name: str,
        class_attribute: List[str],
    ) -> None:
        """
        Same as the method '_replace_string_in_attribute',
        but runs the replacement check on a list of string-attributes

        Args:
            class_name: Name of this list attribute
            class_attribute: Value of this list attribute

        Returns:
            None
        """

        new_list: List[str] = copy.deepcopy(class_attribute)

        for index, class_attribute_element in enumerate(class_attribute):
            for key, value in get_current_replacement_map().items():
                # Don't run replacements with empty string
                if value == "":
                    continue

                # Replace the occurrence of the value in the class attribute, if it is
                # a directory
                if key in class_attribute_element:
                    logger.debug(
                        f"Replace '{key}' "
                        f"in list element '{class_attribute_element}' "
                        f"of attribute {class_name} "
                        f"with '{value}'"
                    )

                    new_list[index] = replace_directory_in_path(
                        file_path=class_attribute_element,
                        replacement_key=key,
                        replacement_value=value,
                    )

        self.__dict__[class_name] = new_list

    def _replace_strings_in_attribute_dict(
        self,
        class_name: str,
        class_attribute: Dict[str, Any],
    ) -> None:
        """
        Same as the method '_replace_string_in_attribute', but runs the replacement
        check on a list of string-attributes

        Args:
            class_name: Name of this dictionary attribute
            class_attribute: Value of this dictionary attribute

        Returns:
            None
        """

        new_dict: Dict[str, Any] = copy.deepcopy(class_attribute)

        for index, (class_attribute_key, class_attribute_value) in enumerate(
            class_attribute.items()
        ):
            if isinstance(new_dict[class_attribute_key], str):
                for key, value in get_current_replacement_map().items():
                    # Don't run replacements with empty string
                    if value == "":
                        continue

                    # Replace the occurrence of the value in the class attribute, if it is
                    # a directory
                    if key in new_dict[class_attribute_key]:
                        logger.debug(
                            f"Replace '{key}' "
                            f"in dict entry '{new_dict[class_attribute_key]}' "
                            f"of attribute {class_name} "
                            f"with '{value}'"
                        )
                        new_dict[class_attribute_key] = replace_directory_in_path(
                            file_path=new_dict[class_attribute_key],
                            replacement_key=key,
                            replacement_value=value,
                        )

            elif isinstance(new_dict[class_attribute_key], list) and check_list_type(
                obj=cast(List[str], new_dict[class_attribute_key]), obj_type=str
            ):
                for list_index, list_element in enumerate(
                    new_dict[class_attribute_key]
                ):
                    new_list_element = list_element

                    for key, value in get_current_replacement_map().items():
                        # Don't run replacements with empty string
                        if value == "":
                            continue

                        # Replace the occurrence of the value in the class attribute, if it is
                        # a directory
                        if key in list_element:
                            logger.debug(
                                f"Replace '{key}' "
                                f"in dict list entry {list_element} "
                                f"of {class_name} "
                                f"with '{value}'"
                            )
                            new_list_element = replace_directory_in_path(
                                file_path=list_element,
                                replacement_key=key,
                                replacement_value=value,
                            )

                    new_dict[class_attribute_key][list_index] = new_list_element

        self.__dict__[class_name] = new_dict

    def check_values(self) -> bool:
        """
        Placeholder method that is intended to be used to check any attribute
        for correct values.

        Returns:
            Whether the attributes contain valid values or not
        """

        return True

    def check_mutual_exclusive(
        self, mutual_attribute_map: Dict[str, List[str]]
    ) -> None:
        """
        Ensures that the mutual-exclusivity defined by the 'mutual_attribute_map'
        is fulfilled for this configuration object.

        mutual_attribute_map FORMAT:
        CLASS_NAME = class name for which to define mutual exclusive parameters
        VALUE = list of names of the attributes as strings

        Example:
        mutual_attribute_map = {
            CLASS_NAME: ["ATTRIBUTE_1", "ATTRIBUTE_2"]
        }

        Args:
            mutual_attribute_map: The dictionary that states which attributes should be handled
                                  mutual exclusively

        Returns:
            None
        """

        if self.__class__.__name__ in mutual_attribute_map:
            check_mutual_attributes_list = mutual_attribute_map[self.__class__.__name__]

            if len(check_mutual_attributes_list) > 0:

                class_attributes = vars(self)

                found_exclusive_items = []

                for check_mutual_attribute in check_mutual_attributes_list:
                    if check_mutual_attribute in class_attributes:
                        if class_attributes[check_mutual_attribute] is not None:
                            found_exclusive_items.append(check_mutual_attribute)
                    else:
                        raise ValueError(
                            f"The class '{type(self)}' "
                            f"does not have the attribute '{check_mutual_attribute}'\n"
                            f"Possible attributes are: {class_attributes.keys()}"
                        )

                if len(found_exclusive_items) > 1:
                    raise ValueError(
                        f"mutual exclusive validated for class '{self.__class__.__name__}', "
                        f"found attributes: {found_exclusive_items}"
                    )

    def _update_string_replacement(
        self,
    ) -> None:
        """
        Recursively checks if this configuration object contains attributes which match
        the name of the keys  of the given globally defined replacement map
        and sets the appropriate value if it is fulfilled.

        Returns:
            The updated string_replacement_map
        """

        replacement_map = get_current_replacement_map()

        if isinstance(self, BaseConfigClass):
            class_attributes = vars(self)

            for class_attribute, value in class_attributes.items():
                if (
                    class_attribute in replacement_map
                    and replacement_map[class_attribute] != value
                ):
                    logger.debug(
                        f"Set placeholder '{class_attribute}' "
                        f"from '{replacement_map[class_attribute]}' to "
                        f"'{value}' taken from class type '{self.__class__.__name__}'"
                    )
                    set_replacement_map_value(key=class_attribute, value=value)

    def recursive_check_mutuality_and_update_replacements(
        self,
        no_checks: bool,
        mutual_attribute_map: Dict[str, List[str]],
    ) -> None:
        """
        Recursively checks if the configuration object violates against any definition of the
        mutual exclusiveness for its attributes. Besides, it is checked if any attribute name
        it contained in the globally defined string replacement map. If that's the case, the
        value of the replacement map is updated accordingly.

        Args:
            no_checks:
            mutual_attribute_map:

        Returns:
            None
        """

        # Update the globally defined string-replacement-map
        self._update_string_replacement()

        if not no_checks:
            # Update the mutual attribute with the one defined for this config class
            if hasattr(self, "mutual_attribute_map"):
                mutual_attribute_map.update(self.mutual_attribute_map)

            # Check if config items are mutually exclusive as stated in the definition
            self.check_mutual_exclusive(mutual_attribute_map)

        class_attributes = vars(self)

        for class_name, class_attribute in class_attributes.items():
            if class_attribute is not None:

                if type(class_attribute) == TypedSequence:
                    for seq_item in class_attribute:
                        if isinstance(seq_item, BaseConfigClass):
                            seq_item.recursive_check_mutuality_and_update_replacements(
                                no_checks=no_checks,
                                mutual_attribute_map=mutual_attribute_map,
                            )
                else:
                    if isinstance(class_attribute, BaseConfigClass):
                        class_attribute.recursive_check_mutuality_and_update_replacements(
                            no_checks=no_checks,
                            mutual_attribute_map=mutual_attribute_map,
                        )

    def recursive_check_values(
        self,
    ) -> None:
        """
        Recursively calls the 'check_values(...)' method of this configuration object.

        Raises:
            A ValueError is raised when any call fails

        Returns:
            None
        """

        class_attributes = vars(self)

        for class_name, class_attribute in class_attributes.items():
            if class_attribute is not None:

                if type(class_attribute) == TypedSequence:
                    for seq_item in class_attribute:
                        if isinstance(seq_item, BaseConfigClass):
                            seq_item.recursive_check_values()
                            if not seq_item.check_values():
                                raise ValueError(
                                    f"Check for attribute '{class_name}' failed!"
                                )
                else:
                    if isinstance(class_attribute, BaseConfigClass):
                        class_attribute.recursive_check_values()
                        if not class_attribute.check_values():
                            raise ValueError(
                                f"Check for attribute '{class_name}' failed!"
                            )
