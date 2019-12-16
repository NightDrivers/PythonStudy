# -*- coding: utf-8 -*-
import re
import json


def func1():
    a = 5


if __name__ == '__main__':
    a = 1
    func1()
    print(a)
    dic = {'a': "b", "c": 1}
    b = json.dumps(dic)
    print(repr(b))
    c = json.loads(b)
    print(c)
    d = "a.b.c"
    e = d.split(".")
    print(e)
