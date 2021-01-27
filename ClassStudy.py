
class A:
    def __init__(self):
        self.a = 1

    def desc(self):
        print("class A desc: " + str(self.a))


class B:
    def __init__(self):
        self.a = 2
        self.b = 2

    def desc(self):
        print("class B desc: " + str(self.a))


class C(A, B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        self.c = 3

    def desc(self):
        print("class C desc: " + str(self.a))


class D:
    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b

    def __repr__(self):
        return "a={} b={}".format(self.a, self.b)


if __name__ == '__main__':
    d = D(b=2, a=1)
    print(d)
