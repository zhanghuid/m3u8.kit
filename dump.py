#!/usr/bin/python
# -*- coding: UTF-8 -*-

from util import get_har
import time
from pprint import pprint


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("url is required")
        exit()

    url = sys.argv[1]
    start = time.time()
    pprint(get_har(url))
    end = time.time()
    print('程序执行时间: ', end - start)
