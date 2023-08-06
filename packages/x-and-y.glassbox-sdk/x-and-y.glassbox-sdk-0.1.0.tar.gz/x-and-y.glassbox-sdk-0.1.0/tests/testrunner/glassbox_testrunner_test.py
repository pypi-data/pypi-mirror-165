from unittest import TestCase


class GlassBoxTestRunnerTest(TestCase):

    def test_abc(self):
        print("test")
        self.assertEqual(1, 1)