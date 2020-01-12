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

import argparse
from pathlib import Path
from typing import Tuple, List
import sys

import cmd

import cmakedebugger.variables as variables

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


class _Wrapper:

    def __init__(self, fd):
        self.fd = fd

    def readline(self, *args):
        try:
            line = self.fd.readline(*args)
        except KeyboardInterrupt:
            print()
            line = '\n'
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
        super().__init__(stdin=_Wrapper(sys.stdin))
        self.use_rawinput = False
        self.intro = "CMakeDebuggerUtily. Type help or ? to list commands.\n"
        self.prompt = "(cmake) "
        self.__parse_cmake_debugger(binary_dir)


    def __parse_cmake_debugger(self, binary_dir:Path) -> None:
        """Parse the CMakeDebugger file and load everything in the REPL."""
        data = read_file(binary_dir)
        data = data[4:]  # The first 4 lines can be ignored
        self.defined_variables: dict = variables.deserialize_variables(data)

    # Commands to execute ###################################################
    def do_var(self, arg: str):
        """Get the value of a CMake variable.

        Example:
            var CMAKE_BUILD_TYPE
        """
        try:
            print(self.defined_variables[arg].value)
        except KeyError:
            print(f"Variable {arg} not found")

    def do_listall(self, arg: str):
        """List all the CMake variables."""
        for name, variable in self.defined_variables.items():
            print(f"{name}={variable.value}")

    def do_exit(self, arg: str):
        """Exit the breakpoint."""
        sys.exit(0)



def main():
    parser = argparse.ArgumentParser(description="CMake debugger")
    parser.add_argument(
        "--binary-dir", required=True, type=Path, help="CMake binary directory"
    )

    args = parser.parse_args()

    repl = CMakeDebugger(args.binary_dir)

    repl.cmdloop()

if __name__== "__main__":
  main()
