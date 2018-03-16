#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, io, os, bs4, requests, re, time, threading
from lxml import etree

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

# 抓取页面内容函数
def down_html(web_url, next_page_tag):
    global index
    # 获取页面内容
    web_res = requests.get(web_url)
    web_res.encoding = 'UTF-8' #改变编码

    try:
        web_res.raise_for_status()
    except Exception as err:
        print('Error:' + err)
        sys.exit('Over')


    html_text = web_res.text
    html_bs = bs4.BeautifulSoup(html_text,'html.parser')

    # 下载图片
    imgObj = html_bs.select('img')
    for img in imgObj:
        img_src = img.get('src')
        img_src = get_real_url(img_src)
        print(img_src)

        image_file_path = down_file(img_src, file_root)

        html_text = html_text.replace(img.get('src'),'../'+image_file_path,1)


    # 下载css
    cssObj = html_bs.select('link')
    for css in cssObj:
        css_rel = css.get('rel') #奇怪，为什么是数组
        # print(css_rel)
        css_href = css.get('href')
        if css_rel[0] == 'stylesheet' and css_href:
            css_href = get_real_url(css_href)
            print(css_href)

            css_file_path = down_file(css_href, file_root)

            html_text = html_text.replace(css.get('href'), '../' + css_file_path, 1)


    # 下载js
    jsObj = html_bs.select('script')
    for js in jsObj:
        js_src = js.get('src')
        if js_src:
            js_src = get_real_url(js_src)
            print(js_src)

            js_file_path = down_file(js_src, file_root)

            html_text = html_text.replace(js.get('src'), '../' + js_file_path, 1)


    # 处理目录url
    contentsObj = html_bs.select('#leftcolumn a')
    for contents in contentsObj:
       html_text = html_text.replace(contents.get('href'), contents.get('href').split('/')[-1], 1)


    # 创建线程写入文件
    # 生成网页文件
    file_name_re = re.search(r'.*/([a-zA-Z0-9-.]+)',web_url)
    file_name = file_name_re.group(1)

    print('Start:' + str(index))
    thread_list = []
    threadObj =  threading.Thread(target=create_html_file, args=(file_name, html_text.encode('utf-8')))
    thread_list.append(threadObj)
    threadObj.start()

    index = int(index) + 1

    # 下一页
    next_page_obj = html_bs.select(next_page_tag)
    if next_page_obj:
        next_page_url = next_page_obj[0].get('href')
        if re.match('/',next_page_url):
            next_page_url = home_url + next_page_url
        # down_html(next_page_url, next_page_tag)
    else:
        for thread in thread_list:
            thread.join()
        print('Over')




# 生成文件（二进制流写入）
def create_html_file(file_name, content):
    file_name_list = file_name.split('.')
    if file_name_list[-1] != 'html':
        file_name += '.html'
    web_file = open(os.path.join('.', 'html', file_name), 'wb')
    web_file.write(content)
    web_file.close()
    print('End:'+file_name)



# 抓取页面内容函数
def down_html_lxml(web_url, next_page_xpath):
    global index
    # 获取页面内容
    web_res = requests.get(web_url)
    web_res.encoding = 'UTF-8'  # 改变编码

    try:
        web_res.raise_for_status()
    except Exception as err:
        print('Error:' + err)
        sys.exit('Over')

    html_text = web_res.text
    html_etree = etree.HTML(html_text)

    # 下载图片
    imgObj = html_etree.xpath('//img')
    for img in imgObj:
        img_src = img.get('src')
        img_src = get_real_url(img_src)
        print(img_src)

        image_file_path = down_file(img_src, file_root)

        html_text = html_text.replace(img.get('src'), '../' + image_file_path, 1)

    # 下载css
    cssObj = html_etree.xpath('//link')
    for css in cssObj:
        css_rel = css.get('rel')
        css_href = css.get('href')
        if css_rel == 'stylesheet' and css_href:
            css_href = get_real_url(css_href)
            print(css_href)

            css_file_path = down_file(css_href, file_root)

            html_text = html_text.replace(css.get('href'), '../' + css_file_path, 1)

    # 下载js
    jsObj = html_etree.xpath('//script')
    for js in jsObj:
        js_src = js.get('src')
        if js_src:
            js_src = get_real_url(js_src)
            print(js_src)

            js_file_path = down_file(js_src,file_root)

            html_text = html_text.replace(js.get('src'), '../' + js_file_path, 1)


    # 处理目录url
    contentsObj = html_etree.xpath("//*[@id='leftcolumn']/a")
    for contents in contentsObj:
        html_text = html_text.replace(contents.get('href'), contents.get('href').split('/')[-1], 1)

    # 创建线程写入文件
    # 生成网页文件
    file_name_re = re.search(r'.*/([a-zA-Z0-9-.]+)', web_url)
    file_name = file_name_re.group(1)

    print('Start:' + str(index))
    thread_list = []
    threadObj = threading.Thread(target=create_html_file, args=(file_name, html_text.encode('utf-8')))
    thread_list.append(threadObj)
    threadObj.start()

    index = int(index) + 1

    # 下一页
    next_page_obj = html_etree.xpath(next_page_xpath)
    if next_page_obj:
        next_page_url = next_page_obj[0].get('href')
        if re.match('/', next_page_url):
            next_page_url = home_url + next_page_url
        down_html_lxml(next_page_url, next_page_xpath)
    else:
        for thread in thread_list:
            thread.join()
        print('Over')


#处理url
def get_real_url(url):
    if re.match('//', url):
        url = 'http:' + url
    elif re.match('/', url):
        url = home_url + url
    return url



#下载文件
def down_file(url,root_path):
    dir = root_path + '/' + '/'.join(url.split('/')[2:-1])
    file_path = dir + '/' + url.split('/')[-1].split('?')[0]

    os.makedirs(dir, 0o777, True)  # True表示忽略已经存在的文件夹
    file = open(file_path, 'wb')
    file.write(requests.get(url).content)

    return file_path



# 生成目录文件（暂时不用）
# def create_contents():
#     index_file = open(os.path.join('.','html','index.html'),'w')
#     html_dir = os.path.join('.','html')
#     for p,d,f in os.walk(html_dir):
#         for ff in f:
#             if ff != 'index.html':
#                 index_file.write('<a href="./'+ff+'">'+ff+'</a><br />')
#     index_file.close()
#     print('End: contents')






############### 执行程序 ###############
#创建目录
if not os.path.isdir('html'):
    os.mkdir('html',0o777)
if not os.path.isdir('files'):
    os.mkdir('files',0o777)

# 首页地址
home_url = 'http://www.runoob.com'
web_url = 'http://www.runoob.com/nodejs/nodejs-tutorial.html'
next_page_tag = ".next-design-link a"
next_page_xpath = "//div[@class='next-design-link']/a"
index = '1'
file_root = 'files'


down_html(web_url, next_page_tag)
# down_html_lxml(web_url, next_page_xpath)


sys.exit('Exit')

