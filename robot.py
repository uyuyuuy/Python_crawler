#!/usr/bin/python

import sys, io, os, bs4, requests, re, time, threading

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

#创建下载目录
# os.mkdir('html',0o777)
# os.mkdir('images',0o777)
# os.mkdir('css',0o777)
# os.mkdir('javascript',0o777)

# 首页地址
home_url = 'http://www.runoob.com'
web_url = 'http://www.runoob.com/nodejs/nodejs-tutorial.html'


# image = re.findall(r'(<img.*>)', home_res.text)
# css = re.findall(r'(<link\s+rel="stylesheet".*>)', home_res.text)
# js = re.findall(r'(<script\s+.*></script>)', home_res.text)


index = '1'
# 抓取页面内容函数
def down_html(web_url):
    global index
    # 获取页面内容
    web_res = requests.get(web_url)
    web_res.encoding = 'UTF-8' #改变编码

    try:
        web_res.raise_for_status()
    except Exception as err:
        print('Error:' + err)


    html_text = web_res.text
    html_bs = bs4.BeautifulSoup(html_text,'html.parser')

    # 下载图片
    imgObj = html_bs.select('img')
    for img in imgObj:
        img_src = img.get('src')
        if re.match('//',img_src):
            img_src = 'http:' + img_src
        if not (re.match('http://',img_src) or re.match('https://',img_src)):
            img_src = home_url + img_src
        print(img_src)

        dir_path = 'files/' + '/'.join(img_src.split('/')[2:-1])
        img_path = dir_path + '/' + img_src.split('/')[-1]

        html_text = html_text.replace(img.get('src'),'../'+img_path,1)

        os.makedirs(dir_path, 0o777, True)  # True表示忽略已经存在的文件夹
        imgBox = open(img_path,'wb')
        imgBox.write(requests.get(img_src).content)


    # 下载css
    cssObj = html_bs.select('link')
    for css in cssObj:
        css_rel = css.get('rel')
        css_href = css.get('href')
        if css_rel[0] == 'stylesheet' and css_href:
            if re.match('//',css_href):
                css_href = 'http:' + css_href
            elif re.match('/',css_href):
                css_href = home_url + css_href
            print(css_href)

            css_dir_path = 'files/' + '/'.join(css_href.split('/')[2:-1])
            css_file_path = css_dir_path + '/' + css_href.split('/')[-1].split('?')[0]

            html_text = html_text.replace(css.get('href'), '../' + css_file_path, 1)

            os.makedirs(css_dir_path, 0o777, True)  # True表示忽略已经存在的文件夹
            cssBox = open(css_file_path,'wb')
            cssBox.write(requests.get(css_href).content)


    # 下载js
    jsObj = html_bs.select('script')
    for js in jsObj:
        js_src = js.get('src')
        if js_src:
            if re.match('//',js_src):
                js_src = 'http:' + js_src
            elif re.match('/',js_src):
                js_src = home_url + js_src
            print(js_src)

            js_dir_path = 'files/' + '/'.join(js_src.split('/')[2:-1])
            js_file_path = js_dir_path + '/' + js_src.split('/')[-1].split('?')[0]

            html_text = html_text.replace(js.get('src'), '../' + js_file_path, 1)

            os.makedirs(js_dir_path, 0o777, True)  # True表示忽略已经存在的文件夹
            jsBox = open(js_file_path,'wb')
            jsBox.write(requests.get(js_src).content)


    # 处理目录
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
    web_content = bs4.BeautifulSoup(html_text, 'html.parser')
    next_page_obj = web_content.select(".next-design-link a")
    if next_page_obj:
        next_page_url = next_page_obj[0].get('href')
        down_html(next_page_url)
    else:
        for thread in thread_list:
            thread.join()
        print('Over')




# 生成文件（二进制流写入）
def create_html_file(file_name, content):
    web_file = open(os.path.join('.', 'html', file_name), 'wb')
    web_file.write(content)
    web_file.close()
    print('End:'+file_name)



# 生成目录（这个不好，舍弃不用）
# def create_contents():
#     index_file = open(os.path.join('.','html','index.html'),'w')
#     html_dir = os.path.join('.','html')
#     for p,d,f in os.walk(html_dir):
#         for ff in f:
#             if ff != 'index.html':
#                 index_file.write('<a href="./'+ff+'">'+ff+'</a><br />')
#     index_file.close()
#     print('End: contents')

down_html(web_url)


sys.exit('Exit')

