import unittest
from .. import settings

class Test测试1(unittest.TestCase):

    def test_1(self):
        result = settings.get("LOG_DIR")
        # self.assertEqual('foo'.upper(), 'FOO')



if __name__ == '__main__':
    unittest.main()
