#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import csv
import os
import pathlib
import queue
import threading

from spider_demo import get_lemma_count, spider_lemmas_by_idx

save_dir = 'spiderdata'  # 保存目录
config_file_dir = 'config_dir'  # 配置文件目录
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
            print(tagid_page_queue.qsize())
            try:
                current_tagid_page = tagid_page_queue.get()
            except tagid_page_queue.Empty:
                continue
            current_file_name = page_file_name_dict.get(current_tagid_page)
            print(current_tagid_page, current_file_name)
            tag_id = current_tagid_page.split('##')[0]
            page = current_tagid_page.split('##')[1]
            spider_lemmas_by_idx(tag_id, current_file_name, page)
            tagid_page_queue.task_done()


def get_page_queues_from_logfile(file):
    '''
    配置队列
    :param file: 待解析的配置文件
    '''
    global page_file_name_dict, tagid_page_queue
    tag_id_names = [line.strip() for line in codecs.open(str(pathlib.Path(config_file_dir, file)),
                                                         encoding='utf-8-sig').readlines() if
                    line.strip()]
    for tag_id_name in tag_id_names:
        tag_id = tag_id_name.split('\t')[0]
        tag_name = tag_id_name.split('\t')[2]
        page = tag_id_name.split('\t')[1]
        tagid_page_queue.put(str(tag_id) + '##' + str(page))
        page_file_name_dict[str(tag_id) + '##' + str(page)] = tag_name
    tagid_page_queue.join()


def get_page_queues(file):
    '''
    配置队列
    :param file: 待解析的配置文件
    '''
    global page_file_name_dict, tagid_page_queue
    tag_id_names = [line.strip() for line in codecs.open(str(pathlib.Path(config_file_dir, file)),
                                                         encoding='utf-8-sig').readlines() if
                    line.strip()]
    for tag_id_name in tag_id_names:
        tag_id = tag_id_name.split('\t')[0]
        tag_name = tag_id_name.split('\t')[1]
        start_page = tag_id_name.split('\t')[2]
        with open(str(pathlib.Path(save_dir, str(tag_name) + '.csv')), 'a+', encoding='utf-8') as entity_file:
            writer = csv.writer(entity_file)
            row = (
                '词条名词',
                '标签名词',
                '词条说明',
                '浏览量',
                'id',
                '链接',
                '词条图片链接',
                '词条图片高度',
                '词条图片宽度'
            )
            writer.writerow(row)
        total_page_str, total_str = get_lemma_count(tag_id)
        if total_str > 50000:
            total_page_str = 501
        for page in range(int(start_page), total_page_str):
            tagid_page_queue.put(str(tag_id) + '##' + str(page))
            page_file_name_dict[str(tag_id) + '##' + str(page)] = tag_name
        tagid_page_queue.join()


if __name__ == '__main__':
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    while not os.path.exists(config_file_dir):
        print('缺少指定配置文件目录！！！' + config_file_dir)
    file_list = os.listdir(config_file_dir)
    while len(file_list) == 0:
        print('配置文件目录中未添加配置文件！！！' + config_file_dir)
    num_worker_threads = 5  # 下载的线程数目
    # 创建线程
    for i in range(num_worker_threads):
        th = spiderThread()
        th.setDaemon(True)
        th.start()
    for file in file_list:
        get_page_queues(file)
