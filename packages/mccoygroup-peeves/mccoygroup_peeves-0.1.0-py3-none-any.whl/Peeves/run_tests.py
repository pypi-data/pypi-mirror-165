"""This is the test running script set up to run all tests
Peeves should be embedded in a project as a submodule at the top level
This will mean there is a "..Tests" package to load the tests from
"""

from .TestUtils import TestManager
TestManager.run(cmd_line=True)
