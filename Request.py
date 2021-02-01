# -*- coding:utf-8 -*-
import requests
# 可用于multipart/form-data格式请求
import requests_toolbelt
import uuid

if __name__ == '__main__':
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    }
    url = "http://southpeak.github.io"
    param = {"headers": header}
    response = requests.get(url, **param)
    print(response.text)

    file = requests.get('https://t7.baidu.com/it/u=2511982910,2454873241&fm=193&f=GIF')
    dest = open(str(uuid.uuid1()), 'wb')
    dest.write(file.content)
