#!/usr/bin/python
# -*- coding: UTF-8 -*-

from json import dumps
import json
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pprint import pprint


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
    har = get_har(url)
    # with open("log_entries.txt", "a") as f:
    #     f.write(json.dumps(proxy.har))
    # pprint(proxy.har)
    urls = []
    for n in har['log']['entries']:
        if ".m3u8" in n['request']['url']:
            print(n['request']['url'])
            urls.append(n['request']['url'])
        # msg = "method: {}, url: {}, query: {}, status: {}".format(
        #     tmp['request']['method'], tmp['request']['url'], tmp['request']['queryString'], tmp['response']['status'])

        # print(msg)
        # with open("log_entries.txt", "a") as f:
        #     f.writelines(msg + "\n")
    
    return urls


def get_har(url):
    # enable headless mode
    options = Options()
    options.set_headless(True)
    # enable proxy
    server = Server(
        # "tools/browserup-proxy-1.2.1/bin/browserup-proxy", {"port": 8060})
        "tools/browserup-proxy-1.2.1/bin/browserup-proxy")
    server.start()
    # proxy = server.create_proxy(
    #     {'captureHeaders': True, 'captureContent': True, 'captureBinaryContent': True})
    proxy = server.create_proxy(
        {'captureHeaders': True, 'captureContent': True})
    profile = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())

    # init browser
    driver = webdriver.Firefox(
        options=options, firefox_profile=profile)

    # dump har
    proxy.new_har(url)
    driver.get(url)
    
    server.stop()
    driver.close()
    return proxy.har


def get_m3u8_v2(url):
    chrome_options = Options()
    # open Browser in maximized mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.binary_location = r'/usr/bin/chromedriver'
    chrome_options.set_headless(True)
    driver = webdriver.Chrome(
        chrome_options=chrome_options)
    driver.get(url)
    JS_get_network_requests = "var performance = window.performance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"
    network_requests = driver.execute_script(JS_get_network_requests)
    for n in network_requests:
        # print(n["name"])
        if ".m3u8" in n["name"]:
            print(n["name"])
    
    driver.close()


def get_m3u8_v3(url):
    chrome_options = Options()
    # open Browser in maximized mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    capabilities = DesiredCapabilities.CHROME
    # capabilities["loggingPrefs"] = {"performance": "ALL"}  # chromedriver < ~75
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+

    driver = webdriver.Chrome(
        options=chrome_options,
        desired_capabilities=capabilities,
    )

    driver.get(url)
    logs = driver.get_log("performance")
    events = process_browser_logs_for_network_events(logs)
    with open("log_entries.txt", "wt") as out:
        for event in events:
            pprint.pprint(event, stream=out)


def process_browser_logs_for_network_events(logs):
    """
    Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
    since we're interested in the network events specifically.
    """
    for entry in logs:
        log = json.loads(entry["message"])["message"]
        if (
                "Network.response" in log["method"]
                or "Network.request" in log["method"]
                or "Network.webSocket" in log["method"]
        ):
            yield log
