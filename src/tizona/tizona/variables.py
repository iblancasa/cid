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
"""Variables module."""
from typing import Tuple, List, Dict

from tizona.errors import SerializedDataError


class CMakeVariable:  # pylint: disable=too-few-public-methods
    """CMake variable."""

    def __init__(self, name: str, value: str):
        """Create a new class instance.

        :param name: name of the variable.
        :param value: value of the variable.
        """
        self.name = name
        self.value = value


def parse_variables(raw_variables: List[str]) -> Dict[str, CMakeVariable]:
    """Parse the variables from the CMakeDebugger file.

    :param raw_variables: all the non-processed variables and their values.
    :returns: list of the variables after parsing.
    """

    def parse_variable(line: str) -> Tuple[str, str]:
        """Parse a variable from the CMakeDebugger file.

        :param line: line to parse.
        :returns: the name and the value of the variable.
        """
        fields = line.split("=")
        if fields:
            name = fields[0]
            if len(fields) > 1:
                value = fields[1]
            else:
                value = ""
        else:
            name = value = ""
        return name, value

    variables = {}
    for line in raw_variables:
        name, value = parse_variable(line)
        variables[name] = CMakeVariable(name, value)
    return variables


def deserialize_variables(data: List[str]):
    """Deserialize all the variables from the given list.

    :param data: a list of non-processed variables.
    :returns: a hashable object with the processed variables. They dict key is
        the name of the variable.
    """
    try:
        start = data.index("# Serialized variables")
    except ValueError:
        raise SerializedDataError(
            "The file is not well formed: start not found"
        )

    try:
        end = data.index("# End serialized variables")
    except ValueError:
        raise SerializedDataError("The file is not well formed: end not found")

    return parse_variables(data[start:end])
