# coding=utf-8
import time
import sys


def count(n):
    while n >= 0:
        yield n
        n = n - 1


class A:

    def __init__(self, items):
        self.items = items

    def allitems(self):
        i = 0
        while i < len(self.items):
            yield self.items[i]
            i = i + 1


if __name__ == '__main__':
    a = A([1, "a", "b", "c", 3, 10, "hello", "world"])
    for item in a.allitems():
        print(item)
