#!/usr/bin/python
# -*- coding: UTF-8 -*-

from json import dumps
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def success(data = []):
    return dumps({
        "status": True,
        "data": data
    })


def fail(msg = ""):
    return dumps({
        "status": False,
        "msg": msg
    })


def get_m3u8(url):
    # enable headless mode
    options = Options()
    options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # enable proxy
    server = Server("tools/browserup-proxy-1.1.0/bin/browserup-proxy")
    server.start()
    # proxy = server.create_proxy(
    #     {'captureHeaders': True, 'captureContent': True, 'captureBinaryContent': True})
    proxy = server.create_proxy(
        {'captureHeaders': True, 'captureContent': True})
    profile = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())

    # init browser
    driver = webdriver.Firefox(
        firefox_options=options, firefox_profile=profile)

    # dump har
    proxy.new_har(url)
    driver.get(url)
    # with open("log_entries.txt", "a") as f:
    #     f.write(json.dumps(proxy.har))
    # pprint(proxy.har)
    urls = []
    for n in proxy.har['log']['entries']:
        if ".m3u8" in n['request']['url']:
            print(n['request']['url'])
            urls.append(n['request']['url'])
        # msg = "method: {}, url: {}, query: {}, status: {}".format(
        #     tmp['request']['method'], tmp['request']['url'], tmp['request']['queryString'], tmp['response']['status'])

        # print(msg)
        # with open("log_entries.txt", "a") as f:
        #     f.writelines(msg + "\n")
    print(urls)
    print('ok')

    # clean up
    server.stop()
    driver.close()
    return urls
