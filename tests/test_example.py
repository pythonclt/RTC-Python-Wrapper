"""
Empty test file that you can copy-and-paste to simplify your life.
If you want your tests to be run automatically, make sure to include:

    from yourtests import *

in the __main__.py file.
"""
try:
    import unittest2 as unittest
except:
    import unittest

class TestNothing(unittest.TestCase):
    def test_nothing(self):
        """ Simply ensures that the package of tests is working. """
        pass

if __name__=="__main__":
    unittest.main()
