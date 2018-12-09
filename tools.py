#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib
import re

# 保存目录
save_dir = 'spiderdata'
# 配置文件目录
config_file_dir = 'configdir'


def remove_space_line():
    file_list = os.listdir(save_dir)
    for file in file_list:
        print(file)
        tag_id_names = [line.strip() for line in open(str(pathlib.Path(save_dir, file)),
                                                      encoding='utf-8-sig').readlines() if line.strip()]
        with open(str(pathlib.Path(config_file_dir, file)), 'a+', encoding='utf-8-sig') as f:
            for tag_id_name in tag_id_names:
                f.write(tag_id_name + '\n')


def create_tag_id_name_file():
    '''
    通过解析生成的权重文件，获取tagid与标签的对应关系
    :return:
    '''
    lines = [line.strip() for line in open('text3.txt', encoding='utf-8').readlines() if line.strip()]
    with open('tag_id_name.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            tag_id = line.split('\t')[0]
            tag_id_name = eval(line.split('\t')[2])
            tmp = 0
            tmp_key = ''
            for key in tag_id_name.keys():
                value = tag_id_name.get(key)
                if value > tmp:
                    tmp = value
                    tmp_key = key
            f.write(str(tag_id) + '\t' + tmp_key + '\t0\n')
            print(tag_id, tmp_key)


def parser_log_file():
    '''
    解析错误日志，生成重试下载文件
    :return:
    '''
    lines = [line.strip() for line in open('spider_log', encoding='utf-8').readlines() if line.strip()]
    tag_files = [line.strip() for line in open('tag_id_name.txt', encoding='utf-8').readlines() if line.strip()]
    tag_id_name = {}
    for tag_file in tag_files:
        tag_id = tag_file.split('\t')[0]
        tag_name = tag_file.split('\t')[1]
        tag_id_name[tag_id] = tag_name
    with open('tagid_failed.txt', 'w', encoding='utf-8') as tagid_failed_file:
        with open('tagid_page_failed.txt', 'w', encoding='utf-8') as tagid_page_failed_file:
            for line in lines:
                match = re.findall('spider_lemmas_by_idx tag_id:\'\d+\', page:\'\d+\' failed', line)
                if match:
                    tag_id, page = re.findall('spider_lemmas_by_idx tag_id:\'(\d+)\', page:\'(\d+)\' failed', line)[0]
                    if tag_id_name.get(tag_id):
                        print(tag_id, page, tag_id_name[tag_id])
                        tagid_page_failed_file.write(str(tag_id) + '\t' + str(page) + '\t' + tag_id_name[tag_id] + '\n')
                else:
                    tag_id = re.findall('spider_lemmas failed tag_id:\'(\d+)\'', line)[0]
                    if tag_id_name.get(tag_id):
                        print(tag_id, tag_id_name[tag_id])
                        tagid_failed_file.write(str(tag_id) + '\t' + tag_id_name[tag_id] + '\t0\n')


if __name__ == '__main__':
    create_tag_id_name_file()
    parser_log_file()