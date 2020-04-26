# CID: CMake Interface for Debugging

[![Build Status](https://travis-ci.org/iblancasa/cid.svg?branch=master)](https://travis-ci.org/iblancasa/cid)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style:
black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<div>
    <img src="logo.svg"
         alt="cid"
         height="150px"
         align="right">
</div>

## What is this?
Do you know what [CMake](https://cmake.org/) is? From the CMake website:

> CMake is an open-source, cross-platform family of tools designed to build,
test and package software. CMake is used to control the software compilation
process using simple platform and compiler independent configuration files,
and generate native makefiles and workspaces that can be used in the compiler
environment of your choice. The suite of CMake tools were created by Kitware
in response to the need for a powerful, cross-platform build environment for
open-source projects such as ITK and VTK.

CMake is an amazing tool to build your software but sometimes it can be
difficult to understand and debug. [Sysprogs created a debugger for
CMake](https://sysprogs.com/w/introducing-cmake-script-debugger/) but it just
work for Windows. For that reason, CID was created.

CID is a set of tools and scripts to help you to debug your CMake scripts.

## Why "CID"?
"El CID" was a Castilian knight and warlord in medieval Spain. Also,
**C**Make **I**nterface for **D**ebugging.

Each module has a name related to "El CID".

## License
This project is licensed under the [Apache 2.0 license](LICENSE).

```
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
```