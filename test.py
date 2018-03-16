#!/usr/bin/python
# -*- coding: UTF-8 -*-

# print()
import sys

hello = False
if hello == True:
    print('Hello World!')


# 变量的定义
name = 'xiangdong' #字符串
age = 18 #整数
weight = 76.5 #浮点型
hobbies = ['Swimming','Boxing','Hiking','Program'] #兴趣爱好，可变变量用列表
kinsfolk = ('father','mather','sister') #家属，不可变的变量用元组
personal_infomation = {'name':name,'age':age,'hobbies':hobbies,'kinsfolk':kinsfolk} #个人信息，信息太多并且有关联关系，所以用字典

# 变量操作
action_1 = False
if action_1 == True:
    # 字符串、列表、元组、字典的取值
    hobbies_1 = hobbies[0]
    hobbies_2 = hobbies[1]
    hobbies_3 = hobbies[2]
    kinsfolk_1 = kinsfolk[0]
    name = personal_infomation['name']
    age = personal_infomation['age']

    # 字符串列表、元组的截取
    hobbies_x = hobbies[0:3] # 截取第一个到第三个元素
    kinsfolk_x = kinsfolk[0:3]  # 截取第一个到第三个元素

    # 列表、字典的赋值，元组和字符串不可更改
    hobbies.append('new') #在尾部插入元素
    hobbies.insert(0,'new') #在下标前插入元素
    personal_infomation['education'] = 'Undergraduate'

    print(len(name))
    print(len(hobbies))
    print(len(kinsfolk))

    hobbies.sort()
    print(hobbies)

    # 列表的操作
    add_str = ','
    hobbies_str = add_str.join(hobbies)
    kinsfolk_str = add_str.join(kinsfolk)
    print(hobbies_str)
    print(kinsfolk_str)
    # 遍历
    for i in hobbies:
        print(i)


    # 字典的遍历
    for k, i in personal_infomation.items():
        print(k + ':' + str(i))

    # 字典的删除
    del personal_infomation['name']
    personal_infomation.keys() #获取所有键值
    personal_infomation.values() #获取所有值
    personal_infomation.clear() #清空字典
    del personal_infomation #删除字典


#类型转换
change_type = False
if change_type == True:
    age = str(age)
    hobbies = tuple(hobbies)
    kinsfolk = list(kinsfolk)

    print(age) #字符串


add_action = False
if add_action:
    #+的使用，可以连接字符串，进行数字计算，还可以合并列表、元组，但是不能用于字典
    print(1 + 1)
    #print('1'+1) #错误
    print(hobbies + hobbies)
    print(kinsfolk + kinsfolk)

    dict1 = {"name":"york"}
    dict2 = {"age":8}

    print(dict1 + dict2) #字典不能+，无结果


# 函数
def func1(name):
    print(name)

# func1('york')




# 文件操作
file = False
if file == True:
    import os
    #os.removedirs('./file')
    #os.mkdir('./file', 0o755) #创建目录
    file = open('./file/one.txt','w+') #打开文件
    content = file.read()
    print(content)

    print(file.name)
    print(file.tell())
    file.write("我是第一个文件") #写入内容

    file.close()

    os.rename('./file/one.txt','./file/two.txt') #重命名


# 时间 日期
time_action = False
if time_action:
    import time
    print(time.time())
    print(time.localtime(time.time()))




# 邮件发送
smtp_action = False
if smtp_action:
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
    message['From'] = Header("菜鸟教程", 'utf-8')
    message['To'] = Header("测试", 'utf-8')

    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('smtp.qq.com', 465)
        smtpObj.login('842276675@qq.com', 'email4211252719')
        smtpObj.sendmail('842276675@qq.com', '842276675@qq.com', message.as_string())
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")





# name = '香港'
# print(name.encode().decode('gbk'))
# print(name.encode().decode('utf-8'))




# Excel

excel_action = True
if excel_action:
    import openpyxl    #v2.5.0
    wb = openpyxl.load_workbook('list.xlsx')

    sheets = wb.sheetnames
    # print(sheets)
    print(wb.active)
    sheet = wb['Sheet1']
    print(sheet['A1'].value)
    print(sheet['A1'].row)
    print(sheet['A1'].column)
    print(sheet['A1'].coordinate)

    print(sheet.rows[1])
    print(sheet.rows[1])



    sheet['A1'].value = 'erp_push_tps_order_queue'
    # wb.save('list2.xlsx')







sys.exit('Over')



