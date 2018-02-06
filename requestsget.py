#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: mum
@license: Apache Licence 
@contact: shuo502@163.com
@author: ‘yo‘
@site: http://github.com/shuo502
@software: PyCharm
@file: requestsget.py
@time: 2018/2/1 18:02
"""
import requests
import proxymode
import headermode
import threadmode


def geturl(url=None,header=None,proxies=None,timeout=None):

    # proxies={}
    if not proxies:proxies = {}
    if not timeout:timeout=5
    if not header:header=headermode.headers().headers_random()
    if not url:  url = "http://github.com"
    # print("get:  ",  proxies,url,header,timeout)
    try:
        if proxies:
            x = requests.get(url, timeout=timeout,headers=header, proxies=proxies,)
        else:
            x = requests.get(url, timeout=timeout, headers=header)
        global get_req
        # print(x.content.decode("utf8","ignore").encode("gbk","ignore"))
        icontent=x.content
        cont=str(icontent)
        coding=(cont[cont.find("charset")+8:cont.find('"',cont.find("charset")+8)])
        ret=icontent.decode(coding,"ignore")
        get_req.append(ret)
        return str(ret)
    except Exception as a:
        if "time out" in str(a):
            proxymode.check_Proxy_update_ip()
            proxies=proxymode.get_Proxy()
            geturl(url,proxies)
            pass
        # print("get:  ", proxies, url, header, timeout)
        global get_Err
        Err={
            "Err":a,
            "url":url,
            "proxies":proxies,
            "headers":header
        }
        get_Err.append(Err)
        print("check_run_Err:",Err)

def get_url_req():
    global  get_req

    temp_get_req=get_req
    get_ret=[]
    return temp_get_req
def get_url_Err():
    global get_Err
    temp_get_ret=get_Err
    get_Err=[]
    return temp_get_ret
get_req=[]
get_Err=[]

def thread_head_proxy_get(url_list):
    global get_req
    get_req=[]
    task_list=[]
    for i in url_list:
        proxy=proxymode.get_Proxy()
        head=headermode.headers().headers_random()
        arg=(i,head,proxy,)
        print(arg)
        task_list.append(arg)

    threadmode.tasks(taskNo=5,target=geturl,argslist=task_list)
    return get_req
    pass





if __name__ == '__main__':

    # geturl(url="http://baidu.com",header="",proxies="",timeout=3)
    # geturl(url="http://baidu.com")
    x=geturl(url="http://jobs.51job.com/beijing-dcq/98290150.html?s=01&t=0")
    print(x)
    print(get_url_req())
    pass
    # a="12345678a"
    # b=int(a)
    # print(isinstance(b,int))


