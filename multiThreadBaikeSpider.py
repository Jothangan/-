#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import pathlib
import queue
import random
import threading

from spider_demo import spider_lemmas

user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

headers = {'User-Agent': random.choice(user_agent_list)}

# # 百度百科获取根据标签id获取词条
# get_lemmas_url = 'https://baike.baidu.com/wikitag/api/getlemmas'
# # 百度百科获取词条浏览量
# url_lemmapv = 'https://baike.baidu.com/api/lemmapv'
# 保存目录
save_dir = 'spiderdata'
# 配置文件目录
config_file_dir = 'config_dir'

# global variables
VISITED = set()  # 记录某个url是否已经被访问了
TAG_ID_QUEUE = queue.Queue()  # 记录某一分类的所有下载页数
THREAD_LOCK = threading.Lock()  # 用于保护公共变量的锁
TAG_ID_NAME_DICT = {}


class spiderThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.get_lemmas_url = 'https://baike.baidu.com/wikitag/api/getlemmas'
        self.url_lemmapv = 'https://baike.baidu.com/api/lemmapv'
        self.save_dir = 'spiderdata'
        self.config_file_dir = 'config_dir'
        print('%s is created' % self.name)

    def run(self):
        global TAG_ID_NAME_DICT, TAG_ID_QUEUE
        while True:
            print(TAG_ID_QUEUE.qsize())
            try:
                current_tag_id = TAG_ID_QUEUE.get()
            except TAG_ID_QUEUE.Empty:
                continue
            THREAD_LOCK.acquire()  # 获取锁来修改VISITED内容
            try:
                if current_tag_id in VISITED:
                    TAG_ID_QUEUE.task_done()
                    continue
                else:
                    # current_tag_name = TAG_ID_NAME_DICT.get(current_tag_id)
                    VISITED.add(current_tag_id)
            finally:
                THREAD_LOCK.release()
            current_tag_name = TAG_ID_NAME_DICT.get(current_tag_id)
            print(current_tag_id, current_tag_name)
            spider_lemmas(current_tag_id, current_tag_name)


def getTagIds(file):
    global TAG_ID_NAME_DICT, TAG_ID_QUEUE
    tag_id_names = [line.strip() for line in codecs.open(str(pathlib.Path(config_file_dir, file)),
                                                         encoding='utf-8-sig').readlines() if
                    line.strip()]
    for tag_id_name in tag_id_names:
        tag_id = tag_id_name.split('\t')[0]
        tag_name = tag_id_name.split('\t')[1]
        TAG_ID_QUEUE.put(tag_id)
        TAG_ID_NAME_DICT[tag_id] = tag_name


if __name__ == '__main__':
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    while not os.path.exists(config_file_dir):
        print('缺少指定配置文件目录！！！' + config_file_dir)
    file_list = os.listdir(config_file_dir)
    while len(file_list) == 0:
        print('配置文件目录中未添加配置文件！！！' + config_file_dir)
    for file in file_list:
        getTagIds(file)
    thread_num = 5  # 下载的线程数目
    # 创建线程
    for i in range(thread_num):
        th = spiderThread()
        # th.setDaemon(True)
        th.start()


