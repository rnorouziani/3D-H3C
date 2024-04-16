import unittest

if __name__ == '__main__':
    # Discover all test modules starting in the current directory
    tests = unittest.defaultTestLoader.discover(start_dir='.', pattern='Test*.py')
    # Set verbosity to 2 for more detailed output
    testRunner = unittest.TextTestRunner(verbosity=1)
    testRunner.run(tests)