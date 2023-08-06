import unittest

from glassbox_sdk.__tests__.testrunner.glassbox_testrunner_test import GlassBoxTestRunnerTest
from glassbox_sdk.spi.validation import CustomTestRunner


def suite():
    suite = unittest.TestSuite()
    suite.addTest(GlassBoxTestRunnerTest('test_abc'))
    return suite

if __name__ == '__main__':
    runner = CustomTestRunner()
    runner.run(suite())

    print(runner.get_logs())