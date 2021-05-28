import unittest

# Load all tests in this directory
loader = unittest.TestLoader()
suite = loader.discover('.')

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
