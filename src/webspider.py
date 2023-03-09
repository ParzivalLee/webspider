# !/bin/python3
import os
import sys
import threading

import requests
import re
from Spider import Spider

"""
filename webspider.py
description 网站爬虫，可用于获取网站全部静态内容
"""


# 爬取内容
def scrape(params):
    response = requests.get(params['url'])
    # 判断请求状态，如果不是200和301则跳过
    print("url:%s\tstatus code:%d" % (response.url, response.status_code))
    if response.status_code != 200 and response.status_code != 301:
        gotUrl.add(params['url'])
        return

    saveFile(params['url'], response.content)

    # 判断是否为文本内容，是则解析
    if response.encoding:
        urls = set()
        for r_url in url_matches:
            # 将解析的url添加到集合
            urls.update(r_url.findall(response.text))
        urls = urls.difference(gotUrl)

        # 生成新的任务
        for url in urls:

            # 判断url长度是否合法
            if len(url) < 2:
                continue
            # 解析url, 判断url是否来自同一个host, 并且检查其是否完整
            if url.startswith("//"):
                if host in url:
                    url = protocol + url
                else:
                    continue
            elif url.startswith("/") and url[1] != "/":
                url = protocol + "//" + host + "/" + url
            else:
                if host in url:
                    url = url
                else:
                    continue

            print("parsed url:\t", url)
            params = dict()
            params['url'] = url
            spider.tasks.append({'function': scrape, 'params': params})


# 保存到文件
def saveFile(url, content):
    url = url.rstrip("/")
    paths = url.split("/")[2:]
    if len(paths) > 1:
        path = '/'.join(paths[:-2])
    else:
        path = paths[0]
    # 文件夹不存在则新建
    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + '/' + paths[-1], 'wb') as fp:
        fp.write(content)


"""
脚本执行
"""

args = sys.argv[1:]

# 编译正则表达式
url_matches = list()
url_matches.append(re.compile(r"href=\"{0,1}([^><\"\' ]*)\"{0,1}"))
url_matches.append(re.compile(r"src=\"{0,1}([^><\"\' ]*)\"{0,1}"))

# 解析参数
start_url = args[0]

# 解析地址
url_sep = start_url.split("/")
print("start url:", start_url)
protocol = url_sep[0]
print("protocol:", protocol)
host = url_sep[2]
print("host:", host)

# 已获取的网址，存于集合， 避免重复
gotUrl = set()

# 蜘蛛类
threadNumber = 5
spider = Spider()

# 生成任务
spider.tasks.append({'function': scrape, 'params': {'url': start_url}})

# 生成线程
for i in range(threadNumber):
    threading.Thread(target=spider.start).start()
