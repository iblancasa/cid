# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Targets module."""
from typing import List, Dict

from tizona.errors import SerializedDataError


class TargetProperty:  # pylint: disable=too-few-public-methods
    """CMake target property."""

    def __init__(self, name: str, value: str):
        """Create a new class instance.

        :param name: name of the target property.
        :param value: value of the target property.
        """
        self.name = name
        self.value = value


class CMakeTarget:  # pylint: disable=too-few-public-methods
    """CMake target.

    :ivar str name: target name.
    :ivar List[TargetProperty] properties: list of target properties.
    """

    def __init__(self, name: str):
        """Create a new class instance.

        :param name: name of the target.
        """
        self.name = name
        self.properties: List[TargetProperty] = []


def parse_target(target_information: List[str]) -> CMakeTarget:
    """Parse a single target.

    :param target_information: all the lines with the serialized target.
    :returns: the serialized target.
    """
    name = target_information[0].replace("++++", "").strip()

    properties = []
    for target_property in target_information[1:]:
        prop_name, value = target_property.lstrip(f"{name} ").split("=")
        properties.append(TargetProperty(prop_name, value))

    target = CMakeTarget(name)
    target.properties = properties
    return target


def parse_targets(raw_targets: List[str]) -> Dict[str, CMakeTarget]:
    """Parse the targets from the CMakeDebugger file.

    :param raw_targets: all the non-processed targets and their values.
    :returns: list of the variables after parsing.
    """
    targets = {}

    matching_targets = filter(lambda x: x.startswith("++++"), raw_targets)
    for target in matching_targets:
        start = raw_targets.index(target)
        finish = raw_targets.index(target.replace("++++", "----"))
        parsed_target = parse_target(raw_targets[start: finish - 1])
        targets[parsed_target.name] = parsed_target
    return targets


def deserialize_targets(data: List[str]) -> Dict[str, CMakeTarget]:
    """Deserialize all the targets from the given list.

    :param data: a list of non-processed targets.
    :returns: a hashable object with the processed targets. They dict key is
        the name of the target.
    """
    try:
        start = data.index("# Serialized targets")
    except ValueError:
        raise SerializedDataError(
            "The file is not well formed: start not found"
        )

    try:
        end = data.index("# End serialized targets")
    except ValueError:
        raise SerializedDataError("The file is not well formed: end not found")

    return parse_targets(data[start:end])
