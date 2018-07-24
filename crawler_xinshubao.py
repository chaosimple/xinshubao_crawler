#!/usr/bin/env python
#coding:utf-8

"""
Purpose: 
    爬取 www.xinshubao.net 上的小说
Authors: 
    Chao -- < chaosimpler@gmail.com >

License: 
    LGPL clause

Created: 
    07/24/18
"""

from __future__ import division
import logging
import numpy as np
import pandas as pd
import codecs
import datetime
import urllib2
from bs4 import BeautifulSoup


#----------------------------------------------------------------------
def get_html(url):
    """该函数用于获取指定链接的远程内容，可能是html页面，也可能是json字符串
    
    
    Arguments :
        url (string) : 远程请求地址
    Returns :
        str_html (string): 字符串；
    Note :
    """
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7"}
    req = urllib2.Request(url,headers=headers)
    str_html = urllib2.urlopen(req).read()
    return str_html

#----------------------------------------------------------------------
def get_chapter_content(url):
    r"""解析指定 URL 的章节内容
        
    Args:
        url (string) : 远程请求地址；
    Returns:
        str_content (string): 指定章节的内容；
    """
    from bs4.element import Tag
    
    str_content = ''
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    
    # 标题内容
    str_title = soup.find('h1').string
    str_content += '\n\n' + u'【' + str_title + u'】' + '\n\n'
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print nowTime
    print str_title
    
    # 章节具体内容
    div = soup.find('div', id = 'content')
    contents = div.contents
    for c in contents:
        if not isinstance(c, Tag):
            if c != '\n':
                str_content += c    
    
    return str_content

#----------------------------------------------------------------------
def append_to_file(str_content, fname):
    r"""将指定内容追加到文件中
        
    Args:
        str_content (string): 要写入文件中的内容；
        fname (string): 文件存储的路径；
    """

    with codecs.open(fname, 'a', 'utf-8') as fa:
        fa.write(str_content)
        fa.write('\n')

#------------------------------------------------------------------------------------------------
def crawl(base_url, start_url, file_name):
    """ 爬取指定页面的内容
    
    思路是：
    指定一个起始页面，抓取该页面的内容，然后找到“下一章”，继续；
    直到“下一章” 对应的超级链接是该小说的章节链接为止；
    
    Args:
        base_url (string): 章节 url 的地址；
        如：http://www.xinshubao.net/12/12962/
        
        start_url (string): 从哪个具体的章节页面开始爬取； 最后一章的“下一章”链接指向base_url；
        如：http://www.xinshubao.net/12/12962/1051402.html
        
        file_name (string): 文件存储的路径；
    """

    # 当前页面的内容
    str_chapter_content = get_chapter_content(start_url)
    append_to_file(str_chapter_content)
    
    # '下一章'的地址
    soup = BeautifulSoup(get_html(start_url), 'lxml')
    next_url = soup.find('a', text = u'下一章')['href']
    
    
    while next_url != base_url:
        
        # 当前页面内容
        next_url = base_url + next_url
        str_chapter_content = get_chapter_content(next_url)
        append_to_file(str_chapter_content)
        
        # '下一章'的地址
        soup = BeautifulSoup(get_html(next_url), 'lxml')
        next_url = soup.find('a', text = u'下一章')['href']        
    
    print 'over.'


if __name__ == '__main__':
    # 《局中迷》
    base_url = 'http://www.xinshubao.net/12/12962/'
    # 第一章
    start_url = 'http://www.xinshubao.net/12/12962/1051402.html'
    # 存储路径
    file_name = '/Users/chao/Downloads/JZM.txt'

    crawl(base_url, start_url, file_name)
    pass