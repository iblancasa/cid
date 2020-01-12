# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# .. macro:: breakpoint()
#
#   call CMakeDebugger breakpoint and serialize some things to
#   ${CMAKE_BINARY_DIR}/CMakeDebugger.
#
#   What is serialized?
#   - All the defined variables (sorted by name) and their values.
#
#
# .. macro:: _serialize_variables()
#
#   :param DEBUGGER_FILE: file where the information will be serialized.
#
#   serialize the variables to the given file. Each variable will be serialized
#   as (one per line): <VARIABLE_NAME>=<VARIABLE_VALUE>.
#

include(CMakeParseArguments)

function(breakpoint)
    set(CMAKE_DEBUGGER_FILE "${CMAKE_BINARY_DIR}/CMakeDebugger")

    # Ensure the file is created
    file(WRITE ${CMAKE_DEBUGGER_FILE}
        "##############################################\n"
        "THIS FILE IS AUTOGENERATED. DO NOT MODIFY IT\n"
        "##############################################\n"
    )

    _serialize_variables(CMAKE_DEBUGGER_FILE ${CMAKE_DEBUGGER_FILE})

endfunction()


function(_serialize_variables)
    cmake_parse_arguments(_SERIALIZE "" "CMAKE_DEBUGGER_FILE" "" ${ARGN})

    file(APPEND ${_SERIALIZE_CMAKE_DEBUGGER_FILE}
        "\n# Serialized variables\n"
    )

    # These are all the defined variables at this point
    get_cmake_property(defined_variables VARIABLES)

    # Sort alphabetically
    list(SORT defined_variables)

    # Serialize to the file
    foreach (defined_variable ${defined_variables})
        file(APPEND ${_SERIALIZE_CMAKE_DEBUGGER_FILE}
            "${defined_variable}=${${defined_variable}}\n"
        )
    endforeach()

    file(APPEND ${_SERIALIZE_CMAKE_DEBUGGER_FILE}
        "\n# End serialized variables\n"
    )

endfunction()
