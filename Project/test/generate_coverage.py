
import unittest
from coverage import Coverage
from glob import glob
import webbrowser
import os


# Generate coverage for all unit tests (File Name: test_*.py)
if __name__ == '__main__':

    # Find all unit test suites
    file_base_names = [os.path.splitext(f)[0] for f in glob('test_*.py')]
    tests = [unittest.defaultTestLoader.loadTestsFromName(module)
             for module in file_base_names]

    # Create single overall test suite
    all_tests = unittest.TestSuite(tests)

    # Run all unit tests with coverage
    cov = Coverage(branch=True, omit='*site-packages*')
    cov.start()
    unittest.TextTestRunner().run(all_tests)
    cov.stop()

    # Generate html report
    cov.html_report()

    # Open in default web browser
    webbrowser.open_new_tab('file://%s' % os.path.abspath('htmlcov/index.html'))
