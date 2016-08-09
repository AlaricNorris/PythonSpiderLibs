#!/usr/local/bin/python
# coding: utf-8

from WeiboLib import WeiboLib
import re
from os import listdir
from os.path import isfile, join


def send_zhihu_post(weibolib, path):
    try:
        f_title = open(path+'/title')
        f_summary = open(path+'/summary')
        f_token = open(path+'/token')

        title = f_title.read().decode('utf-8')
        summary = f_summary.read().decode('utf-8')
        token = f_token.read().decode('utf-8')

        print title,summary,token

        f_title.close()
        f_summary.close()
        f_token.close()

        url = 'http://zhuanlan.zhihu.com/p/' + token
        print 'url',url
        msg = title + '\n   ' + filter_html(summary)
        print 'msg',msg
        msg = msg[0:130] + '|' + url
        print 'msg with url',msg

        # onlyfiles = [ f for f in listdir(path) if isfile(join(path,f)) and f.startswith('screenshot') and f.endswith('.png') ]
        result_files = []
        for i in range(0,9):
            name = 'screenshot'+str(i)+'.png'
            if isfile(join(path, name)):
                result_files.append(join(path, name))
        print result_files

        weibolib.PostWithPics(msg, result_files)
        # print type(msg)
        # print type(encode_to_gb2312(msg))
        print 'post finished'


    except Exception, e:
        print 'got something wrong', e
    finally:
        print 'send zhihu post end'

def send_zhihu_posts(path):
    import os
    import time
    from selenium import webdriver
    driver = webdriver.Chrome()
    weibolib = WeiboLib(driver)
    print 'login'
    weibolib.Login('xxx', 'xxx')

    if os.path.isdir(path):
        print os.listdir(path)
        for p in os.listdir(path):
            print 'sending ',path,'/',p
            send_zhihu_post(weibolib, path+'/'+p)
            time.sleep(30)

    pass

def filter_html(text):
    str = re.sub(r'</?\w+[^>]*>','',text)
    # print str.decode('gb2312').encode('utf-8')
    print str
    return str


def encode_to_gb2312(text):
    try:
        if isinstance(text, unicode):
            text = text.encode('gb2312')
        else:
            text = text.decode('utf-8').encode('gb2312')
    except Exception, e:
        print 'encode error', e
        text = ""
    return text

if __name__ == '__main__':
    # send_zhihu_post('/tmp/zhihu/21722336')
    send_zhihu_posts('/tmp/zhihu')