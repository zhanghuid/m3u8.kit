#!/usr/bin/python
# -*- coding: UTF-8 -*-

from util import get_m3u8
import requests
import time

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("url is required")
        exit()

    url = sys.argv[1]
    start = time.time()
    try:
        headers = requests.head(url)
        if headers.status_code == 404:
            print('有效: \n' + url + '; 状态: ' + 404)
        print('有效:' + url)

    except Exception as e:
        print(str(e))
        print('无效:' + url)

    print("获取 m3u8 列表如下：")
    get_m3u8(url)
    end = time.time()
    print('程序执行时间: ', end - start)
