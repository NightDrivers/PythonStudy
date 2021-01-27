# coding=utf-8

import unittest


class StringEncodeTest(unittest.TestCase):

    def test_str_encode(self):
        temp = u"中文"
        # UTF - 16
        # 生成小端str, 并且带小端bom
        self.assertEqual(temp.encode('UTF-16'), b"\xff\xfe\x2d\x4e\x87\x65")
        # UTF - 16
        # BE大端str不带bom
        self.assertEqual(temp.encode('UTF-16LE'), b"\x2d\x4e\x87\x65")
        # UTF - 16LE
        # 生成小端str不带bom
        self.assertEqual(temp.encode('UTF-16BE'), b"\x4e\x2d\x65\x87")


if __name__ == '__main__':
    unittest.main()
