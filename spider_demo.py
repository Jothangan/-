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
from lxml import etree
import requests
from requests import RequestException
import re
import csv

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '91',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'BIDUPSID=A3134653BE2EEC72BFFFF03DF64F7112; PSTM=1516839947; BAIDUID=BEFBBF7753734AFF962170B0DA309E55:FG=1; BDUSS=B0aEoyUlFMQ0lkcWdvMHdZR3YwNjE5WX5seDRxVX5XUkYyNWxxOEhoajRvZ05jQVFBQUFBJCQAAAAAAAAAAAEAAACEycImZ2FucWlhbzcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPgV3Fv4Fdxbdn; BK_SEARCHLOG=%7B%22key%22%3A%5B%22%E9%99%95%E8%A5%BF%E5%B0%8F%E5%90%83%22%2C%22%E5%BC%A0%E9%AA%9E%22%2C%22%E5%8D%A1%E6%8B%89%E5%93%88%E8%BF%AA%E7%9B%86%E5%9C%B0%22%2C%22%E5%90%B4%E5%A4%A7%E5%87%AF%22%2C%22%E7%8E%84%E5%A5%98%22%2C%22%E7%8E%84%E5%A5%98%E8%A5%BF%E6%B8%B8%22%2C%22%E5%A4%A7%E8%87%AA%E6%B5%81%E7%9B%86%E5%9C%B0%22%2C%22%E5%A1%94%E9%87%8C%E6%9C%A8%E7%9B%86%E5%9C%B0%22%2C%22%E9%A9%AC%E5%85%B6%E5%B4%9B%E8%B5%B7%22%2C%22%E7%9F%AD%E8%82%A0%E8%95%A8%22%2C%22%E5%9C%A3%E6%B5%B7%E4%BC%A6%E4%BF%AE%E6%96%AF%22%2C%22%E5%9C%A3%E6%B5%B7%E4%BC%A6%E4%BF%AE%E6%96%AF%E7%81%AB%E5%B1%B1%22%2C%22%E8%B4%B9%E8%BF%AA%E5%8D%97%E5%A4%A7%E5%85%AC%E9%81%87%E5%88%BA%22%2C%22%E9%9D%92%E9%93%9C%E6%97%B6%E6%9C%9F%22%2C%22%E9%86%8B%E7%BA%BF%E8%99%AB%22%2C%22%E9%9C%B8%E7%8E%8B%E9%BE%99%22%2C%22%E9%9C%B8%E7%8E%8B%E6%81%90%E9%BE%99%22%2C%22%E9%9D%92%E9%93%9C%E9%9B%95%E5%83%8F%22%2C%22%E7%BB%B4%E5%90%BE%E5%B0%94%E6%97%8F%E8%88%9E%22%2C%22%E9%B9%B3%E9%9B%80%E6%A5%BC%22%5D%7D; cflag=15%3A3; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1542245571,1542245610,1542245730,1542680181; pgv_pvi=571139072; pgv_si=s6628707328; bdshare_firstime=1542682002505; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1542703023',
    'Host': 'baike.baidu.com',
    'Origin': 'https://baike.baidu.com',
    'Referer': 'https://baike.baidu.com/wikitag/taglist?tagId=76615',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    "Content-Type": "application/x-www-form-urlencoded",
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}

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
        response = requests.get(url, headers=headers1)
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
    wb_data = requests.post(url, data=data, headers=headers)
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
        json_content = json.loads(content)
        total_page_str = json_content['totalPage']
        total_str = json_content['total']
        print('tagId is {!r}, totalPage is {!r}, total_count is {!r}'
              .format(str(tag_id), str(total_page_str), str(total_str)))
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
tag_id_names = [line.strip() for line in open('tag_id_name.txt', encoding='utf-8').readlines() if line.strip()]
for tag_id_name in tag_id_names:
    tag_id = tag_id_name.split('\t')[0]
    tag_name = tag_id_name.split('\t')[1]
    spider_lemmas(tag_id, tag_name)
print(time.time() - start_time)


# runoobs = [line.strip() for line in open('tag_id_name.txt', encoding='utf-8').readlines() if line.strip()]
# runoobs.sort(key= lambda runoob:int(runoob.split('\t')[2]), reverse=True)
# with open('tag_id_name.txt', 'w', encoding='utf-8') as tag_id_name_file:
#     for runoob in runoobs:
#         tag_id_name_file.write(runoob + '\n')


# lines = [line.strip() for line in open('baike_tag/tag_id_name.txt', 'r', encoding='utf_8') if
#          line.strip() and len(line.split('\t')) == 2]
# for line in lines:
#     tag_id = line.split('\t')[0]
#     paramas = {'limit': 10,
#                'tagId': tag_id,
#                'page': 0}
#     content = get_one_page_by_post(url=get_lemmas_url, data=paramas)
#     json_content = json.loads(content)
#     total_str = json_content['total']
#     print('tagId is {!r}, total_count is {!r}'
#           .format(str(tag_id), str(total_str)))
#     with open('baike_tag/tag_id_name2.txt', 'a+', encoding='utf-8') as tag_id_name:
#         tag_id_name.write(str(total_str) + '\t' + line + '\n')
