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
@file: proxymode.py
@time: 2018/1/31 13:06
"""



import requests
import re
from dbmode import *
from threadmode import *
import headermode


def text_format_proxy(html):
    try:
        a=html.decode('utf8')
    except:
        a=html
    if  len(a)<0:return []
    r = re.compile(r'<tr.*?y"><(.*?)</tr>', re.S)
    n = re.findall(r, a)
    proxyiplist=[]
    def findx(s):
        return s[s.find(">") + 1:s.find("</t")]
    for i in n:
        arri = i.split("<td")
        ip = findx(arri[1])
        port = findx(arri[2])
        art = findx(arri[3])
        ck = findx(arri[4])
        ct = findx(arri[5])

        xdict={"ipport":str(ip)+":"+str(port),"ip":ip, "port":port, "address":art,"other":str(art)+str(ck), "privacy":ck, "itype":ct}
        # print(xdict)
        proxyiplist.append(xdict)
    print("spider ip all is :",len(proxyiplist))
    return proxyiplist



def spider_Proxy(url=""):
    html=""
    iplist = []
    if url=="":
        url= "http://www.xicidaili.com"
    a_web_proxy_list = []
    try:
        import configmode
        webproxy=configmode.webproxy
        print(webproxy)
        for i in webproxy:
            if webproxy[i]:
                a_web_proxy_list.append(str(webproxy[i]+url))
    except:
        pass
    a_web_proxy_list.append(url)
    for url in a_web_proxy_list:
        print(url)
        html = requests.get(url, timeout=5).text  #
        if len(str(html))>800:
            break
        else:
            print("html is null ")
            print("代理无法访问，或服务器无响应")
    # x = open('temp.html', 'rb').read()

    if  html:
        iplist = text_format_proxy(html)
        if iplist:
            insert_ip_t(iplist)



def td_run_proxy_check(httptype,proxyipport,header=""):
    # print("header:  ",header)
    if httptype and proxyipport:
        proxies = {httptype: proxyipport}
        pass
    else:
        print("check_run_proxy Err")
        return "run Err"
    # print("proxies : " , proxies)
    try:
        url="http://github.com"
        x = requests.get(url, timeout=5, proxies=proxies)
        if "dns-prefetch" in x.text and x.status_code<400:
            global check_passip_list
            check_passip.append([proxyipport,httptype])
    except Exception as a:
        pass
        # print("check_run_Err:",a)




def check_Proxy_update_ip(ilist=[]):
    global ip_proxy_list
    ip_proxy_list = []

    if ilist==[]:
        req_tb=find_ip_t()
    else:
        req_tb=ilist
    task_list=[]
    if req_tb:
        head = headermode.headers().headers_random()
        for  i  in req_tb:
            # proxyip=i.ip
            # pport=i.port
            phttp=i.itype
            if "o" in phttp:phttp="HTTPS"
            if "O" in phttp:phttp="HTTPS"
            ipport=i.ipport
            task_list.append((phttp,ipport,head,))

        global check_passip
        check_passip=[]
        if task_list:
            tasks(argslist=task_list,taskNo=10,target=td_run_proxy_check)
        passiplist=check_passip

        if passiplist:
            update_check_ip_t(passiplist)
            print("iplist check ip complete,and pass is  " ,len(passiplist))
        return passiplist


def get_Proxy(a="one"):
    #[[ip:prot, type],]
    global ip_proxy_list
    if not ip_proxy_list:
        lists = find_ispass_ip_t()
        for i in lists:
            if "s" in i[1]:t="HTTPS"
            else:t="HTTP"
            ip_proxy_list.append({t:i[0]})
    if ip_proxy_list and a=="one":
        from random import choice
        o=choice(ip_proxy_list)
        if not o:
            o = choice(ip_proxy_list)
    else:
        o=ip_proxy_list
    return o

    # tb_.update(student_no=tb_.student_no + 1).where(tb_.student_name == 'baby').execute()


check_passip=[]
ip_proxy_list=[]
if __name__ == '__main__':
    # spider_Proxy()

    # y=check_Proxy_update_ip()
    # for i in y:
    #     print(i)
   pass