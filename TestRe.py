# coding=utf-8
import unittest
import re


class ReSampleTest(unittest.TestCase):
    def test_re(self):
        rex = "[\x20-\x7e]+"
        a = "\x12\x20\x21\x22\x12"
        # 从字符串起始位置匹配正则
        match = re.match(rex, a)
        self.assertIsNone(match)
        # 从字符串中查找匹配正则
        match = re.search(rex, a)
        self.assertIsNotNone(match)
        a = "\x20\x21\x22\x12"
        match = re.match(rex, a)
        self.assertIsNotNone(match)

    def test_re_sub(self):
        rex = "abc"
        a = "34abc56abc78abc9ac1ab2bc"
        b = re.sub(rex, "efg", a)
        self.assertEqual(b, "34efg56efg78efg9ac1ab2bc")
        c, d = re.subn(rex, "efg", a)
        self.assertEqual(c, "34efg56efg78efg9ac1ab2bc")
        self.assertEqual(d, 3)

    def test_re_split(self):
        rex = "abc"
        a = "34abc56abc78abc9ac1ab2bc"
        b = re.split(rex, a)
        self.assertEqual(b, ["34", "56", "78", "9ac1ab2bc"])
        a = "abc"
        b = re.split(rex, a)
        self.assertEqual(b, ["", ""])
        a = "abcabcabc"
        b = re.split(rex, a)
        self.assertEqual(b, ["", "", "", ""])

    def test_re_findall(self):
        rex = "[\x20-\x7e]+"
        a = "\x12\x20\x21\x22\x12\x20\x12\x13\x77\x7e\x7f\x45\x46\x47"
        b = re.findall(rex, a)
        print(b)
        self.assertEqual(b, ["\x20\x21\x22", "\x20", "\x77\x7e", "\x45\x46\x47"])
        # 以下两个例子，关于非贪婪模式的猜测
        # 在非贪婪模式下，当找到符合正则的字符串后，马上退出本次匹配，准备进行下一次匹配；
        # 贪婪模式下，找到符合正则的字符串后，依然继续进行当前匹配，继续向后查找,
        # 直到发现字符串添加后一个字符后，不再匹配正则时，才会退出本次匹配，开始下一段匹配
        rex = "\\b\\S+?"
        a = "what is you name"
        b = re.findall(rex, a)
        self.assertEqual(b, ["w", "i", "y", "n"])
        rex = "\\S+?\\b"
        b = re.findall(rex, a)
        self.assertEqual(b, ["what", "is", "you", "name"])


class FormatRexTest(unittest.TestCase):
    def test_re(self):
        rex = '%@|%[#\\-+ 0]?[0-9*]*\\.?[0-9*]*[diouxXfcsb]|%[#\\-+ 0]?[0-9*]*\\.?[0-9*]*L?[fFeEgGaA]'

        text = '已选%#i, 打印%-i份, 预计%+i张, 长度% icm efd%0i'
        resuts = re.findall(rex, text, re.RegexFlag.DOTALL)
        self.assertEqual(resuts, ['%#i', '%-i', '%+i', '% i', '%0i'])

        text = '已选%#12i, 打印%-12i份, 预计%+12i张, 长度% 12icm efd%012i'
        resuts = re.findall(rex, text, re.RegexFlag.DOTALL)
        self.assertEqual(resuts, ['%#12i', '%-12i', '%+12i', '% 12i', '%012i'])

        text = '已选%#12.i, 打印%-12.i份, 预计%+12.i张, 长度% 12.icm efd%012.i'
        resuts = re.findall(rex, text, re.RegexFlag.DOTALL)
        self.assertEqual(resuts, ['%#12.i', '%-12.i', '%+12.i', '% 12.i', '%012.i'])

        text = '已选%#1.1i, 打印%-1.1i份, 预计%+1.1i张, 长度% 1.1icm efd%01.1i'
        resuts = re.findall(rex, text, re.RegexFlag.DOTALL)
        self.assertEqual(resuts, ['%#1.1i', '%-1.1i', '%+1.1i', '% 1.1i', '%01.1i'])

        text = '已选%#.1i, 打印%-.1i份, 预计%+.1i张, 长度% .1icm efd%0.1i'
        resuts = re.findall(rex, text, re.RegexFlag.DOTALL)
        self.assertEqual(resuts, ['%#.1i', '%-.1i', '%+.1i', '% .1i', '%0.1i'])

        text = '已选%#.i, 打印%-.i份, 预计%+.i张, 长度% .icm efd%0.i'
        resuts = re.findall(rex, text, re.RegexFlag.DOTALL)
        self.assertEqual(resuts, ['%#.i', '%-.i', '%+.i', '% .i', '%0.i'])

        text = '已选%#*.*i, 打印%-*.*i份, 预计%+*.*i张, 长度% *.*icm efd%0*.*i'
        resuts = re.findall(rex, text, re.RegexFlag.DOTALL)
        self.assertEqual(resuts, ['%#*.*i', '%-*.*i', '%+*.*i', '% *.*i', '%0*.*i'])

        text = '已选%W, 打印%@份, 预计%T张, 长度%Hcm efd%%i'
        resuts = re.findall(rex, text, re.RegexFlag.DOTALL)
        self.assertEqual(resuts, ['%@', '%i'])


if __name__ == '__main__':
    unittest.main()
