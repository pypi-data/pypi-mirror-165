import unittest

class EmuemuJPTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_main(self):
        from ..emuemuJP import main
        expected = 'emuemuJP'
        actual = main()
        self.assertEqual(expected, actual)
