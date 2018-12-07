#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-19 15:03:00
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

# re_simple_compiled.py

import json
import random
import pathlib
import time
import codecs
from lxml import etree
import requests
from requests import RequestException
import re
import csv

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

headers = {
    'User-Agent': random.choice(user_agent_list)}
headers1 = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}


def get_one_page(url, encoding='utf-8'):
    '''
    获取一个页面
    :param url:
    :param encoding:
    :return:
    '''
    try:
        response = requests.get(url, headers=headers1, timeout=30)
        response.encoding = encoding
        if response.status_code == 200:
            return response.text
        else:
            print(response.status_code)
            return None
    except RequestException:
        print(RequestException.args)
        return None


def get_one_page_by_post(url, data):
    wb_data = requests.post(url, data=data, headers=headers, timeout=30)
    wb_data.encoding = ('UTF-8')
    content = wb_data.text
    return content


get_lemmas_url = 'https://baike.baidu.com/wikitag/api/getlemmas'


def spider_lemmas(tag_id, tag_name):
    paramas = {'limit': 100,
               'tagId': tag_id,
               'page': 0}
    try:
        content = get_one_page_by_post(url=get_lemmas_url, data=paramas)
        if content is None or content == '[]':
            return
        json_content = json.loads(content)
        total_page_str = json_content['totalPage']
        total_str = json_content['total']
        print('tagId is {!r}, totalPage is {!r}, total_count is {!r}'
              .format(str(tag_id), str(total_page_str), str(total_str)))
        with open(str(pathlib.Path('spiderdata', str(tag_name) + '.csv')), 'wb+') as entity_file:
            entity_file.write(codecs.BOM_UTF8)
        with open(str(pathlib.Path('spiderdata', str(tag_name) + '.csv')), 'a+', encoding='utf-8') as entity_file:
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
        print(Exception.args)
        spider_lemmas(tag_id, tag_name)


def spider_lemmas_by_idx(tag_id, tag_name, page):
    paramas = {'limit': 100,
               'tagId': tag_id,
               'page': page}
    try:
        content = get_one_page_by_post(url=get_lemmas_url, data=paramas)
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
            print(idx)
            if idx < len(list):
                entity = list[idx]
                lemma_title = entity.get('lemmaTitle')
                lemma_url = entity['lemmaUrl']
                count += get_first_entity_pv(lemma_url, lemma_title)[0]
                num += 1
        avcount = count / num
        if avcount < 10000:
            print('===========')
            return True
        else:
            print('+++++++++++++++')
        for entity in list:
            lemma_desc = entity.get('lemmaDesc')
            lemma_desc = re.sub('[\n\t\r ]*', '', lemma_desc.strip())
            lemma_id = entity.get('lemmaId')
            lemma_title = entity.get('lemmaTitle')
            lemma_url = entity['lemmaUrl']
            lemma_pic = entity['lemmaPic']
            count, tag_names = get_first_entity_pv(lemma_url, lemma_title)
            if lemma_pic != []:
                lemma_pic_url = lemma_pic['url']
                lemma_pic_height = lemma_pic['height']
                lemma_pic_width = lemma_pic['width']
            else:
                lemma_pic_url = ''
                lemma_pic_height = ''
                lemma_pic_width = ''
            with open(str(pathlib.Path('spiderdata', str(tag_name) + '.csv')), 'a+', encoding='utf-8') as entity_file:
                writer = csv.writer(entity_file)
                row = (
                    lemma_title,
                    str(tag_names),
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
        return spider_lemmas_by_idx(tag_id, tag_name, page)

    except Exception:
        print(Exception.args)
        return spider_lemmas_by_idx(tag_id, tag_name, page)


def get_first_entity_pv(url, title):
    print('spider {!r} , url is: {!r}'.format(title, url))
    html = get_one_page(url)
    if html is None:
        return 10001, None
    tag_names = get_tag_name(html)
    newLemmaIdEnc = parse_enc(html)
    count = get_lemmapv(id=newLemmaIdEnc)
    return count, tag_names


def get_tag_name(html):
    selector = etree.HTML(html)
    hrefs = selector.xpath('//*[@id="open-tag-item"]/span')
    if hrefs is None:
        return None
    return [href.xpath('string(.)').strip() for href in hrefs]


def parse_enc(html):
    import re
    ret = re.findall(r'newLemmaIdEnc:\"(.+?)\"', html)
    if len(ret) == 1:
        return ret[0]
    else:
        return ""


def get_lemmapv(id):
    url_baike_lemmapv = url_lemmapv + '?id=' + id + '&r=' + str(random.random())
    print(url_baike_lemmapv)
    content = get_one_page(url=url_baike_lemmapv)
    if content is None:
        return 10001
    json_content = json.loads(content)
    total_page_str = json_content['pv']
    return total_page_str


url_lemmapv = 'https://baike.baidu.com/api/lemmapv'
start_time = time.time()
tag_id_names = [line.strip() for line in codecs.open('tag_id_name.txt', encoding='utf-8-sig').readlines() if line.strip()]
for tag_id_name in tag_id_names:
    tag_id = tag_id_name.split('\t')[0]
    tag_name = tag_id_name.split('\t')[1]
    print(tag_id, tag_name)
    spider_lemmas(tag_id, tag_name)
print(time.time() - start_time)
