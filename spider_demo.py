#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import csv
import json
import os
import pathlib
import random
import re
import time

import requests
from lxml import etree
from requests import RequestException

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

# 百度百科获取根据标签id获取词条
get_lemmas_url = 'https://baike.baidu.com/wikitag/api/getlemmas'
# 百度百科获取词条浏览量
url_lemmapv = 'https://baike.baidu.com/api/lemmapv'
save_dir = 'spiderdata'  # 保存目录
config_file_dir = 'config_dir'  # 配置文件目录


def request_by_get(url, encoding='utf-8'):
    '''
    通过get方式请求
    :param url: 链接
    :param encoding: 编码
    :return:
    '''
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = encoding
        if response.status_code == 200:
            return response.text
        else:
            print(response.status_code)
            return None
    except RequestException:
        print(RequestException.args)
        return None


def request_by_post(url, data, encoding='utf-8'):
    '''
    通过post方式请求
    :param url: 链接
    :param data: post参数
    :return:
    '''
    try:
        response = requests.post(url, data=data, headers=headers, timeout=30)
        response.encoding = encoding
        if response.status_code == 200:
            return response.text
        else:
            print(response.status_code)
            return None
    except RequestException:
        print(RequestException.args)
        return None


def get_lemma_count(tag_id):
    '''
    保存某个标签下词条总量和页面总量
    :param tag_id: 标签id
    '''
    paramas = {'limit': 100,
               'tagId': tag_id,
               'page': 0}
    try:
        content = request_by_post(url=get_lemmas_url, data=paramas)
        if content is None or content == '[]':
            return
        json_content = json.loads(content)
        total_page_str = json_content['totalPage']
        total_str = json_content['total']
        print('tagId is {!r}, totalPage is {!r}, total_count is {!r}'
              .format(str(tag_id), str(total_page_str), str(total_str)))
        return total_page_str, total_str
    except Exception:
        with open(str(pathlib.Path(save_dir, 'spider_log')), 'a+', encoding='utf-8') as spider_log_file:
            spider_log_file.write('spider_lemmas failed tag_id:{!r} \n'.format(str(tag_id)))
        print(Exception.args)
        return 0, 0


def spider_lemmas(tag_id, tag_name):
    '''
    保存某个标签下的所有词条
    :param tag_id: 标签id
    :param tag_name: 权重较高的标签名
    '''
    paramas = {'limit': 100,
               'tagId': tag_id,
               'page': 0}
    try:
        content = request_by_post(url=get_lemmas_url, data=paramas)
        if content is None or content == '[]':
            return
        json_content = json.loads(content)
        total_page_str = json_content['totalPage']
        total_str = json_content['total']
        print('tagId is {!r}, totalPage is {!r}, total_count is {!r}'
              .format(str(tag_id), str(total_page_str), str(total_str)))
        with open(str(pathlib.Path(save_dir, str(tag_name) + '.csv')), 'wb+') as entity_file:
            entity_file.write(codecs.BOM_UTF8)
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
        if total_page_str is not None:
            total_page = int(total_page_str)
            for page in range(0, total_page):
                print('spider tagId:{!r} page:{!r}, total_page:{!r}'.format(str(tag_id), str(page), str(total_page)))
                if spider_lemmas_by_idx(tag_id, tag_name, page):
                    break
    except Exception:
        with open(str(pathlib.Path(save_dir, 'spider_log')), 'a+', encoding='utf-8') as spider_log_file:
            spider_log_file.write('spider_lemmas failed tag_id:{!r} \n'.format(str(tag_id)))
        print(Exception.args)


def spider_lemmas_by_idx(tag_id, tag_name, page):
    '''
    保存某个tag_id下的某一页的所有词条
    :param tag_id: 标签id
    :param tag_name: 获取到的高权重标签名
    :param page: 第几页
    :return: 是否退出查询
    '''
    paramas = {'limit': 100,
               'tagId': tag_id,
               'page': page}
    try:
        content = request_by_post(url=get_lemmas_url, data=paramas)
        if content is None:
            return True
        parsed_json = json.loads(content)
        list = parsed_json['lemmaList']
        if list is None:
            return True
        # 增加探测边界
        count = 0
        num = 0
        # 步长随机，也可以采用逐步减小步长的策略，越到后面浏览量越小
        for idx in range(0, 100, 20):
            if idx < len(list):
                entity = list[idx]
                lemma_title = entity.get('lemmaTitle')
                lemma_url = entity['lemmaUrl']
                count += get_lemma_info(lemma_url, lemma_title)[0]
                num += 1
        avcount = count / num
        if avcount < 10000:
            print('达到边界，停止搜索')
            return True
        print('在边界内开始保存词条信息')
        for entity in list:
            lemma_desc = entity.get('lemmaDesc')
            lemma_desc = re.sub('[\n\t\r ]*', '', lemma_desc.strip())
            lemma_id = entity.get('lemmaId')
            lemma_title = entity.get('lemmaTitle')
            lemma_url = entity['lemmaUrl']
            lemma_pic = entity['lemmaPic']
            count, tag_list = get_lemma_info(lemma_url, lemma_title)
            if lemma_pic != []:
                lemma_pic_url = lemma_pic['url']
                lemma_pic_height = lemma_pic['height']
                lemma_pic_width = lemma_pic['width']
            else:
                lemma_pic_url = ''
                lemma_pic_height = ''
                lemma_pic_width = ''
            with open(str(pathlib.Path(save_dir, str(tag_name) + '.csv')), 'a+', encoding='utf-8') as entity_file:
                writer = csv.writer(entity_file)
                row = (
                    lemma_title,
                    str(tag_list),
                    lemma_desc,
                    str(count),
                    str(lemma_id),
                    lemma_url,
                    lemma_pic_url,
                    str(lemma_pic_height),
                    str(lemma_pic_width)
                )
                writer.writerow(row)

    except requests.exceptions.ChunkedEncodingError as erro:
        print(erro.args)
        with open(str(pathlib.Path(save_dir, 'spider_log')), 'a+', encoding='utf-8') as spider_log_file:
            spider_log_file.write(
                'spider_lemmas_by_idx tag_id:{!r}, page:{!r} failed \n'.format(str(tag_id), str(page)))
        return False

    except Exception:
        print(Exception.args)
        with open(str(pathlib.Path(save_dir, 'spider_log')), 'a+', encoding='utf-8') as spider_log_file:
            spider_log_file.write(
                'spider_lemmas_by_idx tag_id:{!r}, page:{!r} failed \n'.format(str(tag_id), str(page)))
        return False


def get_lemma_info(url, title):
    '''
    获取词条信息
    :param url:词条链接
    :param title: 词条名
    :return: 词条浏览量，词条标签列表
    '''
    print('spider {!r} , url is: {!r}'.format(title, url))
    html = request_by_get(url)
    if html is None:
        return 10001, None
    tag_list = get_tag_list(html)
    newLemmaIdEnc = parse_enc(html)
    count = get_lemmapv(newLemmaIdEnc=newLemmaIdEnc)
    return count, tag_list


def get_tag_list(html):
    '''
    获取词条的标签列表
    :param html: 对应词条的页面
    :return: 对应词条的标签列表
    '''
    selector = etree.HTML(html)
    hrefs = selector.xpath('//*[@id="open-tag-item"]/span')
    if hrefs is None:
        return None
    return [href.xpath('string(.)').strip() for href in hrefs]


def parse_enc(html):
    '''
    通过正则匹配从网页中获取词条的newLemmaIdEnc
    :param html: 对应词条的页面
    :return: 对应词条的newLemmaIdEnc
    '''
    ret = re.findall(r'newLemmaIdEnc:\"(.+?)\"', html)
    if len(ret) == 1:
        return ret[0]
    else:
        return ""


def get_lemmapv(newLemmaIdEnc):
    '''
    获取词条浏览量
    :param newLemmaIdEnc: 经过加密的id
    :return: 词条浏览量
    '''
    url_baike_lemmapv = url_lemmapv + '?id=' + newLemmaIdEnc + '&r=' + str(random.random())
    print(url_baike_lemmapv)
    content = request_by_get(url=url_baike_lemmapv)
    if content is None:
        return 10001
    json_content = json.loads(content)
    total_page_str = json_content['pv']
    return total_page_str

# if not os.path.exists(save_dir):
#     os.mkdir(save_dir)
# while not os.path.exists(config_file_dir):
#     print('缺少指定配置文件目录！！！' + config_file_dir)
# file_list = os.listdir(config_file_dir)
# while len(file_list) == 0:
#     print('配置文件目录中未添加配置文件！！！' + config_file_dir)
# for file in file_list:
#     start_time = time.time()
#     tag_id_names = [line.strip() for line in codecs.open(str(pathlib.Path(config_file_dir, file)),
#                                                          encoding='utf-8-sig').readlines() if
#                     line.strip()]
#     for tag_id_name in tag_id_names:
#         tag_id = tag_id_name.split('\t')[0]
#         tag_name = tag_id_name.split('\t')[1]
#         print(tag_id, tag_name)
#         spider_lemmas(tag_id, tag_name)
#     print(time.time() - start_time)
