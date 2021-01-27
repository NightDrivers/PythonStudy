# coding=UTF-8

if __name__ == "__main__":
    for i in range(11):
        print("{:2d} {:3d} {:4d}".format(i, i*i, i**3))
    a = [1, 2, 3]
    print("{0[0]:2d}{0[0]:2d}{0[2]:2d}".format(a))
    b = {"lich": 100, "lina": 200, "luna": 300}
    print("lich is {lich} year old. lina is {lina} year old. luna is {luna} year old.".format(**b))

