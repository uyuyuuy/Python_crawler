#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8


import os, sys, time, requests, math

from selenium import webdriver


print('开始执行程序')
qq = '842276675'
driver = webdriver.Firefox(executable_path='/Users/xiangdong/Downloads/geckodriver')

#打开qq空间相册页面
print('打开相册列表页面，该页面会自动跳转到登录页面')
driver.get('https://user.qzone.qq.com/{0}/photo'.format(qq))
driver.maximize_window()

time.sleep(2)
driver.switch_to.frame('login_frame')
print('点击快捷登录图标')
driver.find_element_by_xpath("//div[@id='qlogin_list']/a[@class='face']").click()

time.sleep(15)

driver.switch_to.default_content()
js = "var q=document.documentElement.scrollTop=10000"
print('页面滑动到底部')
driver.execute_script(js)
time.sleep(3)
driver.switch_to.frame('app_canvas_frame')

lists = driver.find_elements_by_xpath("//a[@class='c-tx2 js-album-desc-a']")
album_number = len(lists)
print(len(lists))
time.sleep(3)
index = 20
while index < album_number:
    tmp_floot = index / 21
    page = int(math.floor(tmp_floot))

    driver.switch_to.default_content()
    js = "var q=document.documentElement.scrollTop=" + str(425 + 640*page)
    driver.execute_script(js)
    print('相册列表第' + str(page) + '页')
    print(js)
    time.sleep(8)
    driver.switch_to.frame('app_canvas_frame')
    lists = driver.find_elements_by_xpath("//a[@class='c-tx2 js-album-desc-a']")
    print(len(lists))
    print(lists[index].text)
    lists[index].click()
    time.sleep(3)
    driver.switch_to.default_content()
    js = "var q=document.documentElement.scrollTop=425"
    print('页面向上滑动425像素')
    driver.execute_script(js)
    time.sleep(3)
    print('返回相册列表页面')
    driver.back()
    time.sleep(5)
    index += 1

driver.close()
time.sleep(1)
driver.quit()
sys.exit('Over')


