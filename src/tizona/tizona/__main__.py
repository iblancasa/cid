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
"""Tizona command line."""
import argparse
from pathlib import Path
from typing import List
import sys

import cmd

import tizona.variables as variables
import tizona.targets as targets


class DeserializeDataError(Exception):
    """Errors while deserializing the CMakeDebugger file."""


def read_file(binary_dir: Path) -> List[str]:
    """Read the file where everything was serialized.

    :param binary_dir: path where the build system is generating.
    :returns: the lines from the file.
    """
    with open(binary_dir.joinpath("CMakeDebugger")) as debugger:
        data = debugger.readlines()
    return list(map(lambda x: x.strip("\n"), data))


class _Wrapper:  # pylint: disable=too-few-public-methods
    """Help class for the STDIN management."""

    def __init__(self, fd):
        """Create a new class instance.

        :param fd: file descriptor.
        """
        self.fd = fd  # pylint: disable=invalid-name

    def readline(self, *args):
        """Read a line from the file descriptor."""
        try:
            line = self.fd.readline(*args)
        except KeyboardInterrupt:
            print()
            line = "\n"
        if not line:
            print()
            line = "\n"
        return line


class CMakeDebugger(cmd.Cmd):
    """CMakeDebugger REPL."""

    def __init__(self, binary_dir: Path):
        """Create a new class instance.

        :param binary_dir: CMake binary directory.
        """
        super().__init__(stdin=_Wrapper(sys.stdin))  # type: ignore
        self.use_rawinput = False
        self.intro = "CMakeDebuggerUtily. Type help or ? to list commands.\n"
        self.prompt = "(cmake) "
        self.__parse_cmake_debugger(binary_dir)

    def __parse_cmake_debugger(self, binary_dir: Path) -> None:
        """Parse the CMakeDebugger file and load everything in the REPL."""
        data = read_file(binary_dir)
        data = data[4:]  # The first 4 lines can be ignored
        self.defined_variables: dict = variables.deserialize_variables(data)
        self.defined_targets: dict = targets.deserialize_targets(data)

    # Commands to execute ###################################################
    def do_var(self, arg: str):
        """Get the value of a CMake variable.

        Example:
            var CMAKE_BUILD_TYPE
        """
        name = arg.split(" ")[0]
        try:
            print(self.defined_variables[name].value)
        except KeyError:
            print(f"Variable {name} not found")

    def do_listallvars(self, arg: str):
        """List all the CMake variables."""
        if arg:
            print("Error. Command syntax: <listallvars>")
            return
        for name, variable in self.defined_variables.items():
            print(f"{name}={variable.value}")

    def do_target(self, arg: str):
        """Get a single target."""
        if not arg:
            print("Error. Command syntax: target <target_name> <property>")
        elif len(arg.split(" ")) == 1:
            target = self.defined_targets[arg]
            print(f"Defined properties for target '{arg}'")
            for target_property in target.properties:
                print(f"\t{target_property.name} = {target_property.value}")
        else:
            arguments = arg.split(" ")
            target_name = arguments[0]
            property_name = arguments[1]
            target = self.defined_targets[target_name]

            for target_property in target.properties:
                if target_property.name == property_name:
                    print(target_property.value)
                    break
            else:
                print(
                    f"No property {property_name} found for target "
                    f"{target_name}"
                )

    def do_listalltargets(self, arg: str):
        """List all the CMake targets."""
        if arg:
            print("Error. Command syntax: <listalltargets>")
            return

        for name, _ in self.defined_targets.items():
            print(f"{name}")

    def do_exit(self, arg: str):  # pylint: disable=no-self-use
        """Exit the breakpoint."""
        if arg:
            print("Error. Command syntax: <exit>")
            return

        sys.exit(0)


def main():
    """Run the application."""
    parser = argparse.ArgumentParser(description="CMake debugger")
    parser.add_argument(
        "--binary-dir", required=True, type=Path, help="CMake binary directory"
    )

    args = parser.parse_args()

    repl = CMakeDebugger(args.binary_dir)

    repl.cmdloop()


if __name__ == "__main__":
    main()
