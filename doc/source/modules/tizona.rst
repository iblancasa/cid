tizona
======

What is tizona?
---------------
``tizona`` is the module whose mission is to create an interactive session
between CMake and the user to make easier the debuggability of the projects.

Also, `Tizona <https://en.wikipedia.org/wiki/Tizona>`_ is the name of one of
the swords carried by "El Cid".


How it works
------------

Short version
`````````````
The ``CMake`` execution is paused using a call to the ``tizona`` command-line
interface. ``tizona`` will read all the information and allows the user to
interact with CMake interactively.

Long version
````````````
There is a CMake module called ``Tizona.cmake``. That CMake module includes
a macro called ``breakpoint``. When the macro is called, different information
is deserialized from the CMake execution to a file called ``CMakeDebugger``.
``CMakeDebugger`` is created under the CMake binary directory. Finally,
``breakpoint`` calls ``execute_process``
`(check the official CMake documentation)
<https://cmake.org/cmake/help/latest/command/execute_process.html>`_ running
the ``tizona`` command-line application.

When ``tizona`` is invoked, it reads information from the CMake execution,
specially all the information deserialized in the mentioned ``CMakeDebugger``
file. Then, an interactive session is opened.

If the user sets information, a file called ``CMakeSetter.cmake`` is created. 
That file will include some generated CMake code setting the information
desired by the user. When ``tizona`` is closed, the execution of CMake resumes
and ``CMakeSetter.cmake`` is included (loading and executing all the generated 
CMake code).


API
---
.. automodule:: tizona.__main__
    :show-inheritance:
    :inherited-members:
    :members:
    :private-members:

.. automodule:: tizona.variables
    :show-inheritance:
    :inherited-members:
    :members:
    :private-members:
