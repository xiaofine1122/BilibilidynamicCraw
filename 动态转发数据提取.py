#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import urllib.request as urllib2
import urllib
import json
import sqlite3
import random
import webbrowser
import re
import time
from urllib.parse import *

def GetMiddleStr(content,startStr,endStr):
    content=content.decode('utf-8')
    startIndex=content.index(startStr)
    if startIndex>=0:
        startIndex += len(startStr)
    endIndex = content.index(endStr)
    return content[startIndex:endIndex]

def GetUsers():
    global Bilibili_Key
    GetTotalRepost()
    Bilibili_Key = 0
    has_more = 1
    offset = ''
    DynamicAPI = "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost_detail?dynamic_id="+ Dynamic_id
    conn = sqlite3.connect('Bilibili_TMP.db')
    c = conn.cursor()

    while has_more > 0:
        if offset != '':
            Tmp_DynamicAPI = DynamicAPI + '&offset=' + offset
        else:
            Tmp_DynamicAPI = DynamicAPI
        try:
                print("BiliJsonbegin",Tmp_DynamicAPI) 
                BiliJson = json.loads(urllib2.urlopen(Tmp_DynamicAPI).read())
                has_more = BiliJson['data']['has_more']
                if has_more >0 :
                    offset = BiliJson['data']['offset']
                for BiliJson_dict in BiliJson['data']['items']:
                    BiliJson_card =  json.loads(BiliJson_dict['card'])
                    Bilibili_UID = str( BiliJson_card['user']['uid'])
                    Bilibili_Uname = BiliJson_card['user']['uname']
                    Bilibili_Comment =  BiliJson_card['item']['content']
                    Bilibili_Ts = BiliJson_card['item']['timestamp']
                    Bilibili_Sql = "INSERT or REPLACE into Bilibili (UID,Uname,Comment,Ts,ID) VALUES (" + Bilibili_UID + ", '" + Bilibili_Uname + "', '" + Bilibili_Comment + "',' "+ str(Bilibili_Ts) + "', " + str(Bilibili_Key) + ")"
                    c.execute(Bilibili_Sql)
                    conn.commit()
                    Bilibili_Key = Bilibili_Key + 1
        except Exception as reason:
            print('错误的原因是:', str(reason))
            break   

    conn.close()

def GetTotalRepost():
    global Total_count
    global UP_UID
    global UP_NAME
    DynamicAPI = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=" + Dynamic_id
    BiliJson = json.loads(urllib2.urlopen(DynamicAPI).read())
    Total_count = BiliJson['data']['card']['desc']['repost']
    UP_UID = BiliJson['data']['card']['desc']['user_profile']['info']['uid']
    UP_NAME = BiliJson['data']['card']['desc']['user_profile']['info']['uname']
    print("总数:",Total_count) 
    print("抽奖uid:",UP_UID) 
    print("动态up主:",UP_NAME) 

def PrintAll():
    print("用户信息:") 
    conn = sqlite3.connect('Bilibili_TMP.db')
    c = conn.cursor()
    cursor = c.execute("SELECT UID,Uname,Comment,Ts from Bilibili order by Ts asc")
    i = 0
    for row in cursor:
        i =i +1
        time_local = time.localtime(int(row[3]))
        # 转换成新的时间格式
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        print("第", i,"个转发 用户ID:", row[0]," 用户名:", row[1],"转发详情：", row[2], "转发时间：", dt) 
    print("总数:",Total_count) 
    print("抽奖uid:",UP_UID) 

def WriteIntoText():
    print('写入text文件开始')
    
    textname = '转发记录' + str(time.strftime('%Y%m%d %H%M%S',time.localtime(time.time())))
    f = open(textname+'.txt','a',encoding='utf8')
    conn = sqlite3.connect('Bilibili_TMP.db')
    c = conn.cursor()
    cursor = c.execute("SELECT UID,Uname,Comment,Ts from Bilibili order by Ts asc")

    f.write('动态id：'+str(UP_UID)+ '\n')
    f.write('总数：'+str(Total_count)+ '\n')
    f.write('up主名：'+UP_NAME+ '\n')

    i = 0
    for row in cursor:
        i =i +1
        time_local = time.localtime(int(row[3]))
        # 转换成新的时间格式
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        strline = "第"+ str(i)+"个转发 用户ID:"+ str(row[0])+" 用户名:"+ row[1]+" 转发详情："+ row[2]+ " 转发时间："+ dt + '\n'
        f.write(strline)
    f.close
    print('写入text文件完成，文件名：'+textname)


def GetLuckyDog():
    Bilibili_Doge = random.randint(0,Bilibili_Key)
    conn = sqlite3.connect('Bilibili_TMP.db')
    c = conn.cursor()
    cursor = c.execute("SELECT UID from Bilibili where ID=" + str(Bilibili_Doge))
    res = cursor.fetchall()
    suc = True
    if len(res) > 0 :
        suc = True
        cursor.close()
        conn.close()
        conn2 = sqlite3.connect('Bilibili_TMP.db')
        c2 = conn2.cursor()
        info_cursor = c2.execute("SELECT UID,Uname,Comment from Bilibili where ID=" + str(Bilibili_Doge))
        for row in info_cursor:
            print("用户ID:", row[0]) 
            print("用户名:", row[1]) 
            print("转发详情：", row[2], "\n") 
            # bilibili_open = input(TellTime() + "是否打开网页给获奖用户发送私信：（Y/N）");
            # if bilibili_open == "Y":
            #     webbrowser.open("https://message.bilibili.com/#/whisper/mid" + str(row[0]))
            # elif bilibili_open == "y":
            #     webbrowser.open("https://message.bilibili.com/#/whisper/mid" + str(row[0]))
            # elif bilibili_open == "Yes":
            #     webbrowser.open("https://message.bilibili.com/#/whisper/mid" + str(row[0]))
            # elif bilibili_open == "yes":
            #     webbrowser.open("https://message.bilibili.com/#/whisper/mid" + str(row[0]))
            # elif bilibili_open == "是":
            #     webbrowser.open("https://message.bilibili.com/#/whisper/mid" + str(row[0]))
            # elif bilibili_open == "是的":
            #     webbrowser.open("https://message.bilibili.com/#/whisper/mid" + str(row[0]))
        conn2.close()
    else:
        suc = False
        cursor.close()
        conn.close()
        GetLuckyDog()

def DeleteDatabase():
    DB_path = os.getcwd() + os.sep + "Bilibili_TMP.db"
    try:
        os.remove(DB_path)
        print(TellTime() + "正在清理缓存...") 
    except:
        print(TellTime() + "正在清理缓存...")

def CreateDatabase():
    conn = sqlite3.connect('Bilibili_TMP.db')
    c = conn.cursor()
    primary = ''
    inp = input("请选择是否去掉重复的用户 1：去掉重复 2：不去掉 \n")
    if inp == '1':
        primary = 'PRIMARY KEY'
    else:
        pass
    creatsql = '''CREATE TABLE Bilibili
       (UID   {}   NOT NULL,
       Uname           TEXT    NOT NULL,
       Comment           TEXT    NOT NULL,
       ID            INT      NOT NULL,
       Ts           TEXT    NOT NULL);'''.format(primary)
    c.execute(creatsql)
    conn.commit()
    conn.close()

def GetDynamicid():
    s = input("请粘贴您获取到的网址：")
    nums = re.findall(r'\d+', s)
    try:
       bilibili_domain = urlparse(s)[1]
       if bilibili_domain == "t.bilibili.com":
           print(TellTime() + "为纯文本类型动态") 
           return str(nums[0])
       elif bilibili_domain == "h.bilibili.com":
           bilibili_docid = "https://api.vc.bilibili.com/link_draw/v2/doc/dynamic_id?doc_id=" + str(nums[0])
           Dynamic_id = GetMiddleStr(urllib2.urlopen(bilibili_docid).read(),"dynamic_id\":\"","\"}}")
           print(TellTime() + "为画册类型动态") 
           return str(Dynamic_id)
    except:
       print(TellTime() + "您输入的网址有误！") 
       exit()

def TellTime():
    localtime = "[" + str(time.strftime('%H:%M:%S',time.localtime(time.time()))) + "]"
    return localtime

if __name__ == '__main__':
    DeleteDatabase()
    print("+------------------------------------------------------------+") 
    print("|在电脑端登录Bilibli,点击进入个人主页,再点击动态,进入动态页面|") 
    print("|仅支持500条以下内容，多余部分取不到|") 
    print("|点击对应的动态内容，将获取到的网址复制，并粘贴在下方：      |") 
    print("+------------------------------------------------------------+\n") 
    Dynamic_id = str(GetDynamicid())
    TellTime()
    print(TellTime() + "获取动态成功，ID为：" + Dynamic_id) 
    print(TellTime() + "正在获取转发数据中......") 
    CreateDatabase()
    GetUsers()
    print(TellTime() + "获取数据成功！") 
    # print(TellTime() + "中奖用户信息：\n") 
    # GetLuckyDog()
    # PrintAll()
    WriteIntoText()
    DeleteDatabase()