#!usr/bin/env python3
# -*- coding: utf-8 -*-

'scrapy data with multiprocessing'


import json
import requests
from bs4 import BeautifulSoup
import os
import re
import time
import multiprocessing
import math


def init(MAX_PAGE):
    each = math.floor(MAX_PAGE / 4)
    hosts = 'https://www.dailystrength.org'
    start = time.clock()
    print('starting scrapy...')
    multiprocessing.freeze_support()
    p = multiprocessing.Pool(4)
    for i in range(5):
        p.apply_async(multiprocess_task, args=(i, MAX_PAGE, each, hosts))
    p.close()
    p.join()
    print('All processes completed.')
    end = time.clock()
    print('\nThis time catching %d reconds in total.cost time: %sseconds' % (MAX_PAGE * 15, end - start))


def multiprocess_task(pid, MAX_PAGE, each, hosts):
    print('Process %d started...(PID: %s)' % (pid, os.getpid()))
    page = each * pid + 1
    has_content = True
    end_page = page + each
    print(page, has_content, each)
    while has_content and page < end_page and page < MAX_PAGE + 1:
        print('\nProcess %d: page %d started.' % (pid, page))
        req_url = 'https://www.dailystrength.org/group/depression/discussions/ajax?page=%d&limit=15' % page
        # print(req_url)
        req_data = get_data(req_url)
        # print(req_data)
        bs_html = BeautifulSoup(req_data['html'], 'html.parser')
        # print(bs_html)
        real_urls = []
        for newsfeed__title in bs_html.select('h3.newsfeed__title a'):
            real_urls.append(hosts + newsfeed__title['href'])
        # print(real_urls)
        merge_data(real_urls, page)
        print('\nProcess %d: page %d completed.\n\n' % (pid, page))
        has_content = req_data['has_content']
        page += 1
    print('Process %d ended...\n' % pid)


def get_data(req_url):
    req_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }
    req = requests.get(req_url, headers=req_headers)
    req_text = json.loads(req.text)
    return {
        'html': req_text['content'],
        'has_content': req_text['has_content']
    }


def merge_data(real_urls, page):
    index = 0
    for real_url in real_urls:
        index += 1
        print('start catching data %d-%d' % (page, index))
        comments_html = get_comments_html(real_url)
        real_data = merge_comments_html(comments_html)
        real_data['url'] = real_url
        # print(real_data)
        save_data(real_data, page, index)
        print('Getting data %d-%d completed' % (page, index))


def get_comments_html(real_url):
    req_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }
    req = requests.get(real_url, headers=req_headers)
    return BeautifulSoup(req.text, 'html.parser')


def merge_comments_html(comments_html):
    res = {}
    res['title'] = comments_html.select('h1#discussion_title')[0].text
    print('Title: %s is downloading...' % res['title'])
    res['que'] = {}
    res['ans'] = []
    res['que']['author'] = comments_html.select(
        'span.newsfeed__posted-by a')[0].text
    res['que']['date'] = comments_html.select(
        'span.newsfeed__posted-by + time')[0].text
    res['que']['content'] = comments_html.select('.posts__content')[0].text
    comments = comments_html.select('.comments__comment')
    for comment in comments:
        res['ans'].append({'author': comment.select('.comments__name a')[0].text, 'date': comment.select('time')[0].text, 'content': comment.select('.comments__comment-text')[0].text})
    return res


def save_data(real_data, page, index):
    PATH = os.path.abspath('.')
    data = os.path.join(PATH, 'data')
    if not os.path.exists(data):
        os.mkdir(data)
    date_dir = os.path.join(data, real_data['que']['date'].replace('/', '-'))
    if not os.path.exists(date_dir):
        os.mkdir(date_dir)
    reg = re.compile(r'\\|\/|\:|\*|\?|\"|\<|\>|\|')
    try:
        file = os.path.join(date_dir, real_data['title'] + '%d-%d.txt' % (page, index))
        with open(file, 'w', encoding='utf-8') as f:
            f.write('Url: %s\nTitle: %s\nAuthor: %s\nDate: %s\nCotent: %s\n' % (real_data['url'], real_data['title'], real_data['que']['author'], real_data['que']['date'], real_data['que']['content']))
    except:
        # remove the unlegal word in the title
        # filename in windows can't contain \/:*?"<>|
        print('origin filename has unlegal character, auto rename the file...')
        file = os.path.join(date_dir, re.sub(reg, '#', real_data['title']) + '%d-%d.txt' % (page, index))
        with open(file, 'w', encoding='utf-8') as f:
            f.write('Url: %s\nTitle: %s\nAuthor: %s\nDate: %s\nCotent: %s\n' % (real_data['url'], real_data['title'], real_data['que']['author'], real_data['que']['date'], real_data['que']['content']))
    with open(file, 'a', encoding='utf-8') as f:
        for comment in real_data['ans']:
            f.write('Author: %s\nData: %s\nContent: %s\n' %
                    (comment['author'], comment['date'], comment['content']))


if __name__ == '__main__':
    MAX_PAGE = 10
    init(MAX_PAGE)
