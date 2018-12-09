#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os
import pathlib
import queue

import threading
from spider_demo import get_lemma_count, spider_lemmas_by_idx

save_dir = 'spiderdata'  # 保存目录
config_file_dir = 'configdir'  # 配置文件目录
# global variables
tagid_page_queue = queue.Queue()  # 记录某一分类的所有下载页数
thread_lock = threading.Lock()  # 用于保护公共变量的锁
page_file_name_dict = {}


class spiderThread(threading.Thread):
    '''
    爬虫线程
    '''

    def __init__(self):
        threading.Thread.__init__(self)
        print('%s is created' % self.name)

    def run(self):
        global page_file_name_dict, tagid_page_queue
        while True:
            try:
                current_tagid_page = tagid_page_queue.get()
            except tagid_page_queue.Empty:
                continue
            total_page, total_count = get_lemma_count(current_tagid_page)
            with open('tag_file.txt', 'a+', encoding='utf-8') as tag_file:
                if total_count > 0:
                    tag_file.write(current_tagid_page + '\t\t' + str(total_count) + '\n')
            tagid_page_queue.task_done()


def get_page_queues():
    global page_file_name_dict, tagid_page_queue
    for tag_id in range(1, 70000):
        tagid_page_queue.put(str(tag_id))
    tagid_page_queue.join()


if __name__ == '__main__':
    # if not os.path.exists(save_dir):
    #     os.mkdir(save_dir)
    # while not os.path.exists(config_file_dir):
    #     print('缺少指定配置文件目录！！！' + config_file_dir)
    # file_list = os.listdir(config_file_dir)
    # while len(file_list) == 0:
    #     print('配置文件目录中未添加配置文件！！！' + config_file_dir)
    num_worker_threads = 10  # 下载的线程数目
    # 创建线程
    for i in range(num_worker_threads):
        th = spiderThread()
        th.setDaemon(True)
        th.start()
    # for file in file_list:
    #     get_page_queues(file)
    get_page_queues()
