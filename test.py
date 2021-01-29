# -*- coding: utf-8 -*-
import requests
import uuid
import json


if __name__ == '__main__':
    file = requests.get('https://t7.baidu.com/it/u=2511982910,2454873241&fm=193&f=GIF')
    dest = open(str(uuid.uuid1()), 'wb')
    dest.write(file.content)
