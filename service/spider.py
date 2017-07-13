# -*- coding: utf-8 -*-
import sys
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

zizhu_url = 'http://zizhu.ccnu.edu.cn/index.htm'
huaqing_url = 'http://www.ccnuyouth.com/tzgg.htm'
jiaowuchu1 = 'http://jwc.ccnu.edu.cn/index/tzggxs.htm'
jiaowuchu2 = 'http://jwc.ccnu.edu.cn/index/tzggxy.htm'


def get_webview_zizhu():
    """
    :function: get_webview_zizhu

    资助网爬虫(for webview)
    """
    zizhu_page = requests.get(zizhu_url)
    zizhu_html = zizhu_page.content
    zizhu_soup = BeautifulSoup(zizhu_html, "lxml")
    zizhu_list = zizhu_soup.find_all('ul', class_='main-r-x')[0].find_all('li')[:5]
    result_list = []
    for i in zizhu_list:
        title = i.a.contents[0]
        date = i.small.contents[0]
        content_url = ''.join(['http://zizhu.ccnu.edu.cn/', i.a['href']])
        content_page = requests.get(content_url)
        content_html = content_page.content
        content_soup = BeautifulSoup(content_html, "lxml")
        # different pages have different classes for main content
        find_content_1 = content_soup.find('div', id='vsb_content')
        find_content_2 = content_soup.find('div', id='vsb_content_2')
        find_content_6 = content_soup.find('div', id='vsb_content_6')
        find_content_3 = content_soup.find('div', id='vsb_content_3')
        find_content_4 = content_soup.find('div', id='vsb_content_4')
        find_content_5 = content_soup.find('div', id='vsb_content_5')
        find_content_7 = content_soup.find('div', id='vsb_content_7')
        if find_content_1:
            find_content = find_content_1
        elif find_content_2:
            find_content= find_content_2
        elif find_content_6:
            find_content = find_content_6
        elif find_content_3:
            find_content = find_content_3
        elif find_content_4:
            find_content = find_content_4
        elif find_content_5:
            find_content = find_content_5
        elif find_content_7:
            find_content = find_content_7
        removed_img = [x.extract() for x in find_content.findAll('img')]
        removed_a = [x.extract() for x in find_content.findAll('a')]

        content_appendix_url_list = []
        content_appendix_list_all = content_soup.find_all('ul', style='list-style-type:none')
        if content_appendix_list_all:
            content_appendix_list = content_appendix_list_all[0].find_all('li')
        else:
            content_appendix_list = []
        if content_appendix_list:
            for m in content_appendix_list:
                content_appendix_url_list.append(''.join(['http://zizhu.ccnu.edu.cn', m.a['href']]))
        result_list.append({
            'title': title,
            'content': str(find_content),
            'date': date,
            'appendix_list': content_appendix_url_list
        })
    return result_list


def get_webview_huaqing():
    """
    :function: get_webview_huaqing

    华大青年爬虫(for webview)
    """
    huaqing_page = requests.get(huaqing_url)
    huaqing_html = huaqing_page.content
    huaqing_soup = BeautifulSoup(huaqing_html, "lxml")
    huaqing_list = huaqing_soup.find('div', id='content').find_all('li')
    result_list = []
    result_count = 0
    for i in huaqing_list:
        i_a = i.find_all('a')[1]
        if i.a and result_count < 5:
            title = i_a.contents[0]
            date = list(i.strings)[-2].strip()[:11]
            content_url = "http://www.ccnuyouth.com/" + i_a['href']
            content_page = requests.get(content_url)
            content_html = content_page.content
            content_soup = BeautifulSoup(content_html, "lxml")
            find_content = content_soup.find('div', class_='newsBody')
            removed_img = [x.extract() for x in find_content.findAll('img')]
            removed_a = [x.extract() for x in find_content.findAll('a')]
            content_appendix_url_list = []
            content_appendix_list = content_soup.find_all('div', class_='newsBody')[0].find_all('a')
            if content_appendix_list:
                for m in content_appendix_list:
                    if m.has_attr('href'):
                        ahref = m['href']
                        if ahref[:4] == 'http':
                            content_appendix_url_list.append(ahref)
                        elif ahref[:4] == '/sys':
                            content_appendix_url_list.append(''.join(['http://www.ccnuyouth.com', ahref]))
                        elif ahref[:4] == '../.':
                            content_appendix_url_list.append(''.join([content_url, '/../', ahref]))
            result_list.append({
                'title': title,
                'content': str(find_content),
                'date': date,
                'appendix_list': content_appendix_url_list
                })
            result_count += 1
    return result_list


def get_webview_jiaowuchu(get_url):
    """
    :function: get_webview_jiaowuchu

    教务处爬虫(for webview)
    """
    jiaowuchu_page = requests.get(get_url)
    jiaowuchu_html = jiaowuchu_page.content
    jiaowuchu_soup = BeautifulSoup(jiaowuchu_html, "lxml")
    jiaowuchu_list = jiaowuchu_soup.find_all('ul')[11].find_all('li')[:5]
    result_list = []
    for i in jiaowuchu_list:
        title = i.a.contents[0]
        date = i.span.next_sibling.next_sibling.contents[0]
        content_url = 'http://jwc.ccnu.edu.cn' + i.a['href'][2:]
        content_page = requests.get(content_url)
        content_html = content_page.content
        content_soup = BeautifulSoup(content_html, "lxml")
        find_content = content_soup.find('div', class_='xwcon')
        removed_img = [x.extract() for x in find_content.findAll('img')]
        removed_a = [x.extract() for x in find_content.findAll('a')]

        content_appendix_url_list = []
        if content_soup.find_all('ul', style='list-style-type:none'):
            content_appendix_list = content_soup.find_all('ul', style='list-style-type:none')[0].find_all('li')
            if content_appendix_list:
                for p in content_appendix_list:
                    content_appendix_url_list.append(''.join(['http://jwc.ccnu.edu.cn',p.a['href']]))
        result_list.append({
            'title': title,
            'content': str(find_content),
            'date': date,
            'appendix_list': content_appendix_url_list
            })
    return result_list


def get_webview_board():
    """
    :function: get_pretty_all_board

    运行所有爬虫, 返回按时间排序的结果列表(for webview)
    """
    zizhu_list = get_webview_zizhu()
    huaqing_list = get_webview_huaqing()
    jiaowuchu_list = get_webview_jiaowuchu(jiaowuchu1)
    jiaowuchu_list2 = get_webview_jiaowuchu(jiaowuchu2)
    board_list = zizhu_list + huaqing_list +jiaowuchu_list + jiaowuchu_list2
    date_board_list = sorted(board_list, key=lambda d: d.get('date'), reverse=True)
    return date_board_list
