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

include(CMakeParseArguments)

macro(message)
    set(options)
    set(single_value_args)
    set(multi_value_args
        FATAL_ERROR
        SEND_ERROR
        WARNING
        AUTHOR_WARNING
        DEPRECATION
        NOTICE
        STATUS
        VERBOSE
        DEBUG
        TRACE
    )
    cmake_parse_arguments(_MESSAGE
        "${options}"
        "${single_value_args}"
        "${multi_value_args}"
        ${ARGN}
    )

    
    set(enable_color ${CMAKE_COMMAND} -E env CLICOLOR_FORCE=1)
    set(command_prefix ${enable_color} ${CMAKE_COMMAND} -E cmake_echo_color)

    set(red ${command_prefix} --red)
    set(black ${command_prefix} --black)
    set(green ${command_prefix} --green)
    set(yellow ${command_prefix} --yellow)
    set(blue ${command_prefix} --blue)
    set(magenta ${command_prefix} --magenta)
    set(cyan ${command_prefix} --cyan)
    set(white ${command_prefix} --white)

    set(verbosity)
    set(text_message)

    if(_MESSAGE_FATAL_ERROR) # FATAL_ERROR
        set(verbosity FATAL_ERROR)

        execute_process(
            COMMAND
                ${red} --bold --no-newline "[ERROR] ${_MESSAGE_FATAL_ERROR}"
            OUTPUT_VARIABLE
                text_message
        )

    elseif(_MESSAGE_SEND_ERROR) # SEND_ERROR
        if("${CMAKE_VERSION}" VERSION_LESS 3.15)
            set(verbosity FATAL_ERROR)
        else()
            set(verbosity SEND_ERROR)
        endif()

        execute_process(
            COMMAND
                ${red} --bold --no-newline "[SEND_ERROR] ${_MESSAGE_SEND_ERROR}"
            OUTPUT_VARIABLE
                text_message
        )

    elseif(_MESSAGE_DEPRECATION) # DEPRECATION
        if("${CMAKE_VERSION}" VERSION_LESS 3.15)
            set(verbosity DEPRECATION)
        else()
            set(verbosity WARNING)
        endif()

        execute_process(
            COMMAND
                ${yellow} --no-newline "[DEPRECATION] ${_MESSAGE_DEPRECATION}"
            OUTPUT_VARIABLE
                text_message
        )

    elseif(_MESSAGE_NOTICE) # NOTICE
        set(verbosity)
        set(text_message "${_MESSAGE_NOTICE}")

    elseif(_MESSAGE_WARNING) # WARNING
        set(verbosity WARNING)
        execute_process(
            COMMAND
                ${yellow} --bold --no-newline "[WARNING] ${_MESSAGE_WARNING}"
            OUTPUT_VARIABLE
                text_message
        )

    elseif(_MESSAGE_AUTHOR_WARNING) # AUTHOR_WARNING
        set(verbosity AUTHOR_WARNING)
        execute_process(
            COMMAND
                ${yellow} --bold --no-newline "[AUTHOR_WARNING] ${_MESSAGE_WARNING}"
            OUTPUT_VARIABLE
                text_message
        )

    elseif(_MESSAGE_SEND_ERROR) # SEND_ERROR
        set(verbosity SEND_ERROR)
        execute_process(
            COMMAND
                ${red} --bold --no-newline "[SEND_ERROR] ${_MESSAGE_SEND_ERROR}"
            OUTPUT_VARIABLE
                text_message
        )

    elseif(_MESSAGE_VERBOSE) # VERBOSE
        if("${CMAKE_VERSION}" VERSION_LESS 3.15)
            set(verbosity STATUS)
        else()
            set(verbosity VERBOSE)
        endif()

        execute_process(
            COMMAND
                ${green} --bold --no-newline "[VERBOSE] "
            OUTPUT_VARIABLE
                fmt_verbosity
        )

        set(text_message "${fmt_verbosity} ${_MESSAGE_VERBOSE}")

    elseif(_MESSAGE_DEBUG) # DEBUG
            if("${CMAKE_VERSION}" VERSION_LESS 3.15)
                set(verbosity STATUS)
            else()
                set(verbosity DEBUG)
            endif()

        execute_process(
            COMMAND
                ${cyan} --bold --no-newline "[DEBUG] "
            OUTPUT_VARIABLE
                fmt_verbosity
        )

        set(text_message "${fmt_verbosity} ${_MESSAGE_DEBUG}")

    elseif(_MESSAGE_TRACE) # TRACE
        if("${CMAKE_VERSION}" VERSION_LESS 3.15)
            set(verbosity STATUS)
        else()
            set(verbosity TRACE)
        endif()

        execute_process(
            COMMAND
                ${magenta} --bold --no-newline "[TRACE] "
            OUTPUT_VARIABLE
                fmt_verbosity
        )

        execute_process(
            COMMAND
                ${cyan} --bold --no-newline "${_MESSAGE_TRACE}"
            OUTPUT_VARIABLE
                fmt_message
        )
        
        set(text_message "${fmt_verbosity} ${fmt_message}")

    elseif(_MESSAGE_STATUS) # STATUS
        set(verbosity STATUS)

        execute_process(
            COMMAND
                ${green} --no-newline "[STATUS] "
            OUTPUT_VARIABLE
                fmt_verbosity
        )

        set(text_message "${fmt_verbosity} ${_MESSAGE_STATUS}")
    endif()

    _message(${verbosity} "${text_message}")

endmacro()
