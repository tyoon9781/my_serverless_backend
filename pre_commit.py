import unittest
import sys


test_loader = unittest.TestLoader()
suite = test_loader.discover("app/tests", pattern="test_*.py")
runner = unittest.TextTestRunner()
result = runner.run(suite)




if result.wasSuccessful():
    sys.exit(0)
else:
    sys.exit(1)
