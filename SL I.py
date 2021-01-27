# coding=UTF-8
import os
import glob
import re
import math
from datetime import datetime

if __name__ == '__main__':
    os.chdir("/Users/ldc/PycharmProjects/PythonStudy")
    a = os.getcwd()
    a = os.system("pwd")
    print(a)
    b = glob.glob("*.py")
    print(b)
    # sys.argv 参数处理函数
    # c = getopt.getopt(sys.argv)
    # 正则
    rex = r"\bf[a-z]*"
    d = re.findall(rex, "which foot or hand fell fastest")
    print(d)
    # math
    e = math.tan(math.pi/4)
    print(e)
    # urllib2
    # f = urllib2.urlopen("http://10.0.10.220:9999/")
    # g = f.readline()
    # print g
    # date
    h = datetime.today()
    print(h.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %I.%M%p."))
    # python中时间日期格式化符号：
    # % y
    # 两位数的年份表示（00 - 99）
    # % Y
    # 四位数的年份表示（000 - 9999）
    # % m
    # 月份（01 - 12）
    # % d
    # 月内中的一天（0 - 31）
    # % H
    # 24
    # 小时制小时数（0 - 23）
    # % I
    # 12
    # 小时制小时数（01 - 12）
    # % M
    # 分钟数（00 = 59）
    # % S
    # 秒（00 - 59）
    # % a
    # 本地简化星期名称
    # % A
    # 本地完整星期名称
    # % b
    # 本地简化的月份名称
    # % B
    # 本地完整的月份名称
    # % c
    # 本地相应的日期表示和时间表示
    # % j
    # 年内的一天（001 - 366）
    # % p
    # 本地A.M.或P.M.的等价符
    # % U
    # 一年中的星期数（00 - 53）星期天为星期的开始
    # % w
    # 星期（0 - 6），星期天为星期的开始
    # % W
    # 一年中的星期数（00 - 53）星期一为星期的开始
    # % x
    # 本地相应的日期表示
    # % X
    # 本地相应的时间表示
    # % Z
    # 当前时区的名称
    # % % % 号本身
