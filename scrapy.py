#!usr/bin/env python3
# -*- coding: utf-8 -*-

'scrapy data'


import json
import requests
from bs4 import BeautifulSoup
import os
import time
import random

extra_time = 0
timeout = 0
urls = []


def init(MAX_PAGE):
    global has_content
    global extra_time
    global timeout
    start = time.clock()
    # count the like button in each topic and save in one file
    print('starting scrapy...')
    page = 1
    print('Start scrapying Block %s' % block)
    while has_content and page < MAX_PAGE + 1:
        req_url = 'https://www.dailystrength.org/group/%s/discussions/ajax?page=%d&limit=15' % (block, page)
        # print(req_url)
        print('Start scrapying Page %d...' % page)
        try:
            req_data = get_data(req_url)
        except:
            try:
                timeout += 1
                sleep_time = random.randint(3, 5)
                extra_time += sleep_time*60
                print('Time out! Start second try...')
                print('Anti-scrapy: sleep time-%ss' % sleep_time * 60)
                time.sleep(sleep_time * 60)
                req_data = get_data(req_url)
            except:
                print('Time out twice! Pass to next page')
                page += 1
                continue
        # print(req_data)
        bs_html = BeautifulSoup(req_data['html'], 'html.parser')
        # print(bs_html)
        real_urls = []
        for newsfeed__title in bs_html.select('h3.newsfeed__title a'):
            real_urls.append(hosts + newsfeed__title['href'])
        # print(real_urls)
        merge_data(real_urls)
        has_content = req_data['has_content']
        page += 1
    print('All tasks completed.')
    end = time.clock()
    print('\nThis time catching %d reconds in total.cost time: %ss.(PS.%ss was costing in avoiding anti-scrapy). Number of timeout: %d' % (index, end - start, extra_time, timeout))


def get_data(req_url):
    global extra_time
    req_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }
    req = requests.get(req_url, headers=req_headers)
    req_text = json.loads(req.text)
    return {
        'html': req_text['content'],
        'has_content': req_text['has_content']
    }


def merge_data(real_urls):
    global timeout
    global extra_time
    global urls
    for real_url in real_urls:
        if real_url in urls:
            print('the url has been visited. pass to next url.')
            continue
        urls.append(real_url)
        try:
            comments_html = get_comments_html(real_url)
        except:
            try:
                timeout += 1
                sleep_time = random.randint(30, 45)
                extra_time += sleep_time
                print('Time out! Start second try...')
                print('Anti-scrapy: sleep time-%ss' % sleep_time)
                time.sleep(sleep_time)
                comments_html = get_comments_html(real_url)
            except:
                print('Time out twice! Pass to next url...')
                continue
        real_data = merge_comments_html(comments_html)
        real_data['url'] = real_url
        # print(real_data)
        save_data(real_data)


def get_comments_html(real_url):
    # global extra_time
    req_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }
    req = requests.get(real_url, headers=req_headers)
    return BeautifulSoup(req.text, 'html.parser')


def merge_comments_html(comments_html):
    res = {}
    # res['title'] = comments_html.select('h1#discussion_title')[0].text
    # res['like'] = int(comments_html.select('.newsfeed__icon-count')[1].text)
    # print('Title: %s is downloading...' % res['title'])
    res['que'] = {}
    res['ans'] = []
    res['username'] = []
    # res['que']['author'] = comments_html.select('span.newsfeed__posted-by a')[0].text
    # res['que']['date'] = comments_html.select('span.newsfeed__posted-by + time')[0].text
    res['que']['content'] = comments_html.select('.posts__content')[0].text
    comments = comments_html.select('.comments__comment')
    res['username'].append(comments_html.select('.newsfeed__posted-by a')[0].text.lower())
    for each in comments_html.select('.comments__name a'):
        res['username'].append(each.text.lower())
    for comment in comments:
        # res['ans'].append({'author': comment.select('.comments__name a')[0].text, 'date': comment.select('time')[0].text, 'content': comment.select('.comments__comment-text')[0].text})
        text = comment.select('.comments__comment-text')[0].text
        if len(text) < 40:
            continue
        if len(text) > 2000:
            continue
        res['ans'].append({'content': text})
    print('%d comments in total' % (len(res['ans']) + 1))
    with open('username.txt', 'a', encoding='utf8') as f:
        for each in res['username']:
            f.write('%s\n' % each)
    return res


def save_data(real_data):
    global index
    PATH = os.path.abspath('.')
    source = os.path.join(PATH, 'source')
    if not os.path.exists(source):
        os.mkdir(source)
    data = os.path.join(source, block)
    if not os.path.exists(data):
        os.mkdir(data)
    file = os.path.join(data, '[index].txt')
    with open(file.replace('[index]', '{:05d}'.format(index)), 'w', encoding='utf-8') as f:
        if len(real_data['que']['content']) < 2000:
            f.write('%s' % real_data['que']['content'])
            print('NO.%d document download completed.' % index)
            index += 1
    for comment in real_data['ans']:
        with open(file.replace('[index]', '{:05d}'.format(index)), 'w', encoding='utf-8') as f:
            f.write('%s\n' % comment['content'])
        print('NO.%d document download completed.' % index)
        index += 1


if __name__ == '__main__':
    index = 1020
    hosts = 'https://www.dailystrength.org'
    has_content = True
    # block = 'lung-cancer'
    # block = 'breast-cancer'
    # block = 'colon-cancer'
    # block = 'diabetes-type-1'
    block = 'diabetes-type-2'
    MAX_PAGE = 15
    init(MAX_PAGE)
