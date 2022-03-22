# m3u8.kit
---
    get requests by input url

## 依赖
1. 谷歌
- 驱动依赖
```
❯ chromedriver --version
ChromeDriver 99.0.4844.51
```

- 浏览器依赖
```
❯ /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
Google Chrome 99.0.4844.51 
```

2. 火狐 
- 驱动依赖 
```
❯ geckodriver --version
geckodriver 0.24.0 ( 2019-01-28)
```
- 浏览器依赖
```
❯ /Applications/Firefox.app/Contents/MacOS/firefox --version
Mozilla Firefox 98.0.1
```

## 使用
### 1. 安装虚拟环境
```
> python3 -m venv venv
> source venv/bin/active
> pip install -r requirements.txt
```
### 2. 使用情况
1. 直接 dump 所有请求 (or 加过滤) [推荐使用]
```
python dump.py http://waipian8.com/play/121461-2-1/ |grep m3u8
```

2. 获取 m3u8 的请求地址 [推荐使用]
```
python m3u8.py http://waipian8.com/play/121461-2-1/ |grep m3u8
```

3. 启动一个服务
```
# 运行服务
> python serve.py

# 测试请求
> curl -v http://localhost:8078/?url=https://icaqd.com/vodplay/343803-1-1.html
```

## 日志
1. 火狐浏览器日志
```
tail -100f ./geckodriver.log
```

2. 服务 browser-proxy 日志
```
tail -100f ./server.log
```


## 引用
1. [file-dump_har-py](https://gist.github.com/dino-su/29d2646d41acf6aab1546b982a727f42#file-dump_har-py)
2. [Supported platforms](https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html)
3. [browserup-proxy-py](https://github.com/browserup/browserup-proxy-py)