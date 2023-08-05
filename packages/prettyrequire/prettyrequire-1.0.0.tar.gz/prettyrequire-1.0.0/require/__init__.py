"""
prettyrequire.

Conditional control made pretty.
require(condition, message) will raise an exception if condition is false.
"""

__version__ = "1.0.0"
__author__ = 'TheCookingSenpai'

def require(condition, message):
    if not condition:
        print("REQUIRE: " + message)
        raise Exception(message)
    