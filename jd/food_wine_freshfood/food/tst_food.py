__author__ = 'huafeng'
#coding:utf-8
import os
import re
import time
import codecs
import urllib2
from bs4 import BeautifulSoup

PATH = os.path.dirname(os.path.abspath(__file__))

jd_list_root_url = 'http://list.jd.com/'
def read_one_page_url_to_get_pagesize():
    url_end_with_pagesize = True
    if url_end_with_pagesize:
        page_size_div_pattern = page_size_div_pattern = re.compile(r'''<div class=\\"pagin pagin-m\\">.*?/(?P<page_size>\d+)</span>''')
    else:
        page_size_div_pattern = re.compile(r'''<div class='pagin pagin-m'>.*?/(?P<page_size>\d+)</span>.*?href="(?P<end_url_pattern>[\d\-]+.html)"''', re.S)
    url = "http://list.jd.com/list.html?cat=1320,5019,5020"
    html = urllib2.urlopen(url).read()
    match_str = page_size_div_pattern.search(html)
    page_size = match_str.group('page_size')
    print page_size
    # splited_url = end_url.split('-')
    # splited_url[12] = '%s'
    # end_url_pattern = '-'.join(splited_url)
    # for page_num in range(1, int(page_size)+1):
    #     url = ''.join((jd_list_root_url,end_url_pattern%str(page_num)))
    #     print url
    # page_size_str = page_size_div_pattern.search(html).group(1) if page_size_div_pattern.search(html) else ''
    # if not page_size_str:
    #     print "no html match page_size here in url:%s"%url
    #     return
    # print page_size_str
    # for page_count in range(1, int(page_size_str)+1):
    #     page_url = "&".join((url,'page=%s'%page_count))
    #     print page_url
# read_one_page_url_to_get_pagesize()
def parse_page_url_pattern_from_html():
    html = '''<LI><a href='http://list.jd.com/list.html?cat=1315,1346,12039'>领带/领结/领带夹</a></LI>'''
    match = re.search(r"href='(http.*?)'", html)
    if match:
        print match.group(1)
    else:
        print match
# parse_page_url_pattern_from_html()
def gen_whole_root_page_url():
    url_pattern = re.compile(r"href='(http.*?)'")
    one_root_page_url = 'http://list.jd.com/list.html?cat=1320,5019,5020'
    html = urllib2.urlopen(one_root_page_url).read()
    li_str_list = re.findall(r'<LI>.*?</LI>', html)
    whole_root_page_url_list = [url_pattern.search(item).group(1) for item in li_str_list]
    print whole_root_page_url_list, len(whole_root_page_url_list)
    return whole_root_page_url_list
# gen_whole_root_page_url()
def write_whole_page_url_into_file(page_url_list):
    filename = os.path.join(PATH, 'sys', 'whole_page_url')
    with codecs.open(filename, mode='a', encoding='utf-8') as af:
        temp_list_to_write = [item+'\n' for item in page_url_list]
        af.writelines(temp_list_to_write)
def gen_whole_page_url():
    url_end_with_pagesize = True
    jd_list_root_url = 'http://list.jd.com/'
    if url_end_with_pagesize:
        page_size_div_pattern = page_size_div_pattern = re.compile(r'''<div class=\\"pagin pagin-m\\">.*?/(?P<page_size>\d+)</span>''')
    else:
        page_size_div_pattern = re.compile(r'''<div class='pagin pagin-m'>.*?/(?P<page_size>\d+)</span>.*?href="(?P<end_url_pattern>[\d\-]+.html)"''', re.S)
    whole_root_page_url = gen_whole_root_page_url()
    url_count = 0

    for root_page_url in whole_root_page_url:
        url_count += 1
        whole_page_url_list = []
        html = urllib2.urlopen(root_page_url).read()
        if url_end_with_pagesize:
            page_size_str = page_size_div_pattern.search(html)
            total_page_size = page_size_str.group('page_size')
            print url_count, total_page_size
            for page_size in range(1, int(total_page_size)+1):
                page_url = '&'.join((root_page_url, 'page=%s'%page_size))
                whole_page_url_list.append(page_url)
            # print whole_page_url_list
            # time.sleep(5)
        else:
            match_str = page_size_div_pattern.search(html)
            try:
                page_size, end_url = match_str.group('page_size', 'end_url_pattern')
            except:
                page_size,end_url = 0,False
            print url_count, page_size
            if end_url and page_size:
                splited_url = end_url.split('-')
                splited_url[12] = '%s'
                end_url_pattern = '-'.join(splited_url)
                whole_page_url_list.extend([''.join((jd_list_root_url,end_url_pattern%str(page_num))) for page_num in range(1, int(page_size)+1)])
            else:
                whole_page_url_list.append(root_page_url)
            # print whole_page_url_list
            # time.sleep(5)
        write_whole_page_url_into_file(whole_page_url_list)
gen_whole_page_url()
def read_one_page_url_to_get_item_id():
    url = "http://list.jd.com/6233-6291-6306-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-33.html"
    html = urllib2.urlopen(url).read()
    item_id_list = re.findall(r"sku='(\d+)'><div class=", html)
    print item_id_list, len(item_id_list)
    # item_id_list = [re.search("[\d]+", item).group() for item in item_id_str_list]
    # print item_id_list, len(set(item_id_list))
    # temp_list_for_write = [item+'\n' for item in item_id_list]
# read_one_page_url_to_get_item_id()
def get_whole_item_id():
    ITEM_FILENAME = 'food_item_id'
    ip_port = '222.66.115.233:80'
    http_hanlder = urllib2.ProxyHandler({'http':'http://%s'%ip_port})
    opener = urllib2.build_opener(http_hanlder)
    urllib2.install_opener(opener)
    whole_page_url_filename = os.path.join(PATH, 'sys', 'whole_page_url')
    crawled_page_url_filename = os.path.join(PATH, 'log', 'crawled_page_url')
    failed_page_url_filename = os.path.join(PATH, 'log', 'failed_item_id')
    item_id_filename = os.path.join(PATH, 'sys', ITEM_FILENAME)
    with codecs.open(whole_page_url_filename, encoding='utf-8') as whole_page_url_f,\
    codecs.open(crawled_page_url_filename, mode='wb', encoding='utf-8') as crawled_page_wf, \
    codecs.open(failed_page_url_filename, mode='wb', encoding='utf-8') as failed_page_url_wf, \
    codecs.open(item_id_filename, mode='wb', encoding='utf-8') as item_id_wf:
        for page_url in whole_page_url_f.readlines():
            try:
                html = urllib2.urlopen(page_url.strip(), timeout=15).read()
            except:
                try:
                    html = urllib2.urlopen(page_url.strip(), timeout=15).read()
                except:
                    failed_page_url_wf.write('timeout in url;%s'%page_url)
                    continue
            end_url_with_pagesize = False
            if end_url_with_pagesize:
                item_id_list = re.findall(r'''sku=\\"(\d+)\\" selfservice''', html)
            else:
                item_id_list = re.findall(r"sku='(\d+)'><div class=", html)
            if not item_id_list:
                failed_page_url_wf.write('not match id_str in url;%s'%page_url)
                continue
            temp_list_for_write = [item+'\n' for item in item_id_list]
            item_id_wf.writelines(temp_list_for_write)
            crawled_page_wf.write(page_url)
            # print temp_list_for_write
            # time.sleep(3)
# get_whole_item_id()
