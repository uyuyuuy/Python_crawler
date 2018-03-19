#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8


import os, sys, time, requests, math

from selenium import webdriver


print('开始执行程序')
qq = '842276675'
driver = webdriver.Chrome()

#打开qq空间相册页面
print('打开相册列表页面，该页面会自动跳转到登录页面')
driver.get('https://user.qzone.qq.com/{0}/photo'.format(qq))
driver.maximize_window()

time.sleep(2)
driver.switch_to.frame('login_frame')
print('点击快捷登录图标')
driver.find_elements_by_xpath("//div[@id='qlogin_list']/a[@class='face']")[1].click()

time.sleep(15)

driver.switch_to.default_content()
js = "var q=document.documentElement.scrollTop=10000"
print('页面滑动到底部')
driver.execute_script(js)
time.sleep(2)
driver.switch_to.frame('app_canvas_frame')

lists = driver.find_elements_by_xpath("//a[@class='c-tx2 js-album-desc-a']")
album_number = len(lists)
print(len(lists))
time.sleep(2)
index = 7
while index < album_number:
    driver.switch_to.default_content()
    js = "var q=document.documentElement.scrollTop=0"
    driver.execute_script(js)
    time.sleep(1)

    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    time.sleep(1)

    tmp_floot = index / 8
    page = int(math.floor(tmp_floot))

    js = "var q=document.documentElement.scrollTop=" + str(445 + 240*page)
    driver.execute_script(js)
    print(js)
    print('相册列表第' + str(page) + '页')
    time.sleep(2)

    driver.switch_to.frame('app_canvas_frame')
    lists = driver.find_elements_by_xpath("//a[@class='c-tx2 js-album-desc-a']")
    print(len(lists))
    print(lists[index].text)

    #进入相册详情页面
    lists[index].click()
    time.sleep(1)
    js = "var q=document.documentElement.scrollTop=0"
    driver.execute_script(js)
    time.sleep(2)

    #定位到图片列表
    driver.switch_to.default_content()

    js = "var q=document.documentElement.scrollTop=10000"
    print('页面滑到底部')
    driver.execute_script(js)
    time.sleep(2)

    js = "var q=document.documentElement.scrollTop=340"
    print('页面向上滑动340像素')
    driver.execute_script(js)
    time.sleep(2)

    driver.switch_to.frame('app_canvas_frame')
    images = driver.find_elements_by_xpath("//ul[@class='list j-pl-photolist-ul']/li")
    




    print('返回相册列表页面')
    driver.back()
    time.sleep(1)
    index += 1

driver.close()
time.sleep(1)
driver.quit()
sys.exit('Over')


