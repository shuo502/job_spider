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
@file: run_main.py
@time: 2018/1/31 13:07
"""
import requests
import configmode as cf
import dbmode as dbs
import headermode as head
import proxymode as prox
import threadmode as tdm

# requests.
# class req():
#     def __init__(self,get):
#         self.req=requests
#         # self.header=""
#
#     def header(self):
#         return self.req.header()
#
#     def con(self):
#         return self



import threadmode,headermode,proxymode,conf.conf51job

import requestsget
def spider_list():
    threadmode.tasks(target=requestsget.geturl,argslist=conf.conf51job.main_page(1, 5),taskNo=2)
    html_list=requestsget.get_url_req()
    Err=requestsget.get_url_Err()
    if Err:print(Err)
    spider_dom_info_list_list = []
    for i in html_list:
        if  i:
            spider_dom_info_list_list.append(conf.conf51job.text_company_format(i))
    #[[],[],]
    spider_dom_info_list=[]
    for i in spider_dom_info_list_list:
        for j in i:
            spider_dom_info_list.append(j)
    return spider_dom_info_list #[{},{},]



def spider_list_all(company_opt_list):#[{},{},]
    new_task_dict_list=[]

    for data_dict in company_opt_list:  # 当前页签所有信息的列表
        if data_dict["oid"] in oid_arr:  # 如果当前id在数据库临时列表存在则跳过
            pass
        else:
            new_task_dict_list.append(data_dict)

    print("task all is :",len(new_task_dict_list))
    if new_task_dict_list:
        threadmode.tasks(target=insert_tb_run_cs,taskNo=8,argslist=new_task_dict_list)
        iErr=requestsget.get_url_Err()
        if iErr:
            for i in iErr:
                print("出错信息：",i)
    print("is complete")



def insert_tb_run_cs(data_dict):
    global companyid_arr,oid_arr
    # if  data_dict["oid"] in oid_arr :
    #     return

    head=headermode.headers().headers_random()
    proxy=proxymode.get_Proxy()
    url=data_dict['ourl']

    html=requestsget.geturl(url=url,header=head,proxies=proxy,timeout=5)
    # html = requests.get(url, timeout=5, headers=head,proxies=proxy).content
    # print("req:",requestsget.get_url_req())
    # print("reE",requestsget.get_url_Err())

    n=[]
    if html:
        n = conf.conf51job.text_info_format(html)  # 采集抓取 该url 的详细信息 返回字典
    if n:
        newdict = dict(data_dict, **n)  # 格式化字典
        if src_task_lock.acquire():#资源锁
            if n['xbmsg']: dbs.txErrsor(url=data_dict["ourl"], errtext=newdict['xbmsg'])  # 如果有错误信息，插入错误信息到数据库
            try:
                dbs.position.create(**newdict)  # 插入数据库
                oid_arr.append(data_dict["oid"])  # 插入数据库临时列表
                print("run_insert  :", data_dict["companyname"],data_dict["o"], data_dict["ourl"])
            except:
                pass

            if data_dict["companyid"] in companyid_arr:  # 如果公司数据库里临时列表存在该信息跳过
                pass
                # print(data_dict["companyname"])
            else:

                try:
                    dbs.company_tb.create(**newdict)  # 写入数据库
                    # dbs.closes()
                    companyid_arr.append(data_dict["companyid"])  # 插入到公司数据库临时列表
                    print(data_dict["companyname"])
                except:
                    pass
        src_task_lock.release()  # 解锁


companyid_arr = [str.format(i.companyid) for i in dbs.company_tb.select(dbs.company_tb.companyid)]  # 数据库取出公司名称
oid_arr = [str.format(i.oid) for i in dbs.position.select(dbs.position.oid)]  # 取出职位ID编号
src_task_lock=threadmode.src_task_lock
if __name__ == '__main__':
    # print("spider  Proxy ---------------")
    # proxymode.spider_Proxy()
    # print("check ip---------------")
    # proxymode.check_Proxy_update_ip()
    print("spider_job ---------------")
    pass
    import time
    temp_i=0
    while 1:
        temp_i+=1
        print("spider job page --------")
        t1=time.time()
        a=spider_list()
        print("spider job opt info --------",len(a))
        b=spider_list_all(a)
        if temp_i==12:
            temp_i=0
            proxymode.check_Proxy_update_ip()
        print("task run :", time.time()-t1)
        print("sleep 600s ---------------",temp_i)
        time.sleep(600)



