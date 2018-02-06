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
@file: conf51job.py
@time: 2018/1/31 14:27
"""

#
"""
配置框架
项目
内容处理
数据库配置
特殊代理配置
header配置
线程配置



HTML处理
爬取页面 链接，标题 筛选

爬取 详细信息和介绍 

数据库处理
定义数据库文件
定义数据库表
定义数据库列

代理爬取是否用代理
用哪个模式代理

是否用header 
用哪个header
是否需要自定义获取header

线程
是否多线程


"""
from bs4 import BeautifulSoup

import re



def text_company_format(html):#in html out url and info  type list

    company_opt_list=[]
    try:
        bs=BeautifulSoup(html, 'html.parser').find("div", class_="dw_table").find_all("div", class_="el")
    except:
        pass
    if bs:
        bs.pop(0)
    for b in bs:
        # print(b)
        # print("==---------------------------------------------")
        dictx = {}
        try:
            title = b.find('p', class_='t1').find('a')['title']
            titleurl = b.find('p', class_='t1').find('a')['href']
            companyname = b.find('span', class_='t2').find('a')['title']
            companyurl = b.find('span', class_='t2').find('a')['href']
            worklocate = b.find('span', class_='t3').text
            salary = b.find('span', class_='t4').text
            reposttime = b.find('span', class_='t5').text
            oid = titleurl[titleurl.rfind("/") + 1:titleurl.find(".htm")]
            # if 'jobid' in titleurl or 'php?' in url:
            # if 'jobid' in titleurl:
            if  "jobid" in titleurl:
                oid = titleurl[titleurl.find("jobid=") + 6:]
            if len(oid) > 9:
                oid = str(oid)[:8]
            x = "http://jobs.51job.com/beijing-dcq/{}.html?s=01&t=0"
            titleurl = x.format(oid)
            dictx = {'o': title
                , 'ourl': titleurl
                , 'oid': oid
                , 'worklocate': worklocate
                , 'salary': salary
                , 'reposttime': reposttime
                , 'companyname': companyname
                , 'companyurl': companyurl
                , 'companyid': companyurl[companyurl.rfind('/') + 1:companyurl.find('.htm')] }
        except Exception:
            pass
        company_opt_list.append(dictx)
    return company_opt_list

def text_info_format(html):#in html  out  other info   type dict
    workinfo, locate, companyinfo, ltype, xbmsg = '', '', '', 'x|x|x', []
    companyp, companysp, companyclass = "", "", ""
    ins = BeautifulSoup(html, 'html.parser')
    arr = []
    try:
        bsx = ins.find("div", class_="tCompany_main")
        ltype = ins.find('div', class_='tHeader tHjob').find('p', class_='msg ltype').text
        arr = ltype.replace("\r\n", "").replace(" ", "").replace("\xa0", "").replace("\t", "").split("|")
        companyinfo = bsx.find('div', class_='tmsg inbox').text
        workinfo = bsx.find('div', class_='bmsg job_msg inbox').text
        xbmsgi = bsx.find_all('div', class_='bmsg inbox')
        locate = bsx.find('div', class_='bmsg inbox').find('p', class_='fp').text
        # tx=xbmsgi
        # print((tx))
        if locate == "": xbmsg = xbmsgi
        if len(xbmsgi) > 1:
            xbmsg = str(xbmsgi)
            print(xbmsg)
            # print(url)
        # print(xbmsgi)
    except Exception:
        pass

    for i in arr:
        if '0人' in i:
            companyp = i
        else:
            if companysp == "":
                for j in ['资', '企', '司', '单', '政', '组']:
                    if j in i:
                        companysp = i
            else:
                companyclass = i

    xdict = {'workinfo': workinfo,
             'locate': locate.replace("\r\n", "").replace(" ", "").replace("\xa0", "").replace("\t", ""),
             'companyinfo': companyinfo,
             'xbmsg': xbmsg,
             'companyclass': companyclass,
             'companysp': companysp,
             'companyp': companyp
             }
    # print("conf51job info fomate:",xdict)
    return xdict



def main_page(start,end):
    # companyid_arr= [str.format(i.companyid) for i in dbs.company_tb.select(dbs.company_tb.companyid)]#数据库取出公司名称
    # oid_arr= [str.format(i.oid) for i in dbs.position.select(dbs.position.oid)]#取出职位ID编号
    # url = "http://search.51job.com/list/010000,000000,0000,00,9,99,%2B,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=05%2C09%2C11&degreefrom=99&jobterm=99&companysize=01%2C02&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="
    url='http://search.51job.com/list/010000,000000,0000,00,9,99,%2B,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=01%2C02&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=8&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    urls = [url.format(p) for p in range(start, end+1)]#生成url 页签数组
    return urls




if __name__ == '__main__':
    pass


