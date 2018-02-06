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
@file: dbmode.py
@time: 2018/1/31 13:05
"""

import  peewee

from peewee import *
db=SqliteDatabase('51job.db')
class company_tb(Model):
    companyname=CharField(null=False,verbose_name='公司名')
    companyid=CharField(null=False,verbose_name="公司id",unique=True)
    companyurl=CharField(null=False,verbose_name='公司页面')
    locate=CharField(null=True,verbose_name='公司地址')
    companyinfo=TextField(null=True,verbose_name='公司信息')
    companyclass=CharField(null=True,verbose_name='公司行业')
    companysp=CharField(null=True,verbose_name='公司类型')
    companyp=CharField(null=True,verbose_name='公司规模')
    class Meta:
        database=db


class position(Model):
    o=CharField(null=False,verbose_name='岗位名称')
    ourl=CharField(null=False,verbose_name='岗位链接')
    oid=CharField(null=False,verbose_name='岗位id',unique=True)
    worklocate=CharField(null=True,verbose_name='工作地点')
    salary=CharField(null=True,verbose_name='待遇')
    reposttime=CharField(null=True,verbose_name='刷新时间')
    companyname=CharField(null=True,verbose_name='公司名称')
    companyurl=CharField(null=True,verbose_name='公司链接')
    companyid=CharField(null=True,verbose_name='公司id')
    workinfo=TextField(null=True,verbose_name='职位信息')
    pass
    class Meta:
        database=db


class txErrsor(Model):
    url = CharField(verbose_name="url")
    errtext = TextField(verbose_name='内容')
    othe = TextField(verbose_name="othe")
    class Meta:
        database = db



try:company_tb.create_table()
except:pass
try:position.create_table()
except:pass
try:txErrsor.create_table()
except: pass

#
# class connect(Model):
#     class   Meta:
#         try:
#             database=db
#             db.connect()
#         except:
#             pass
#
# class closes(Model):
#     class Meta:
#         try:
#             database=db
#             database.close()
#         except:
#             pass


proxydb=SqliteDatabase("proxydb.db")

class tb_ip_p(Model):
    ipport=CharField(verbose_name="ip端口",null=False,max_length=22,unique=True)
    ip=CharField(verbose_name="ip",null=False,max_length=15,unique=False)
    port=CharField(verbose_name="端口",null=False,max_length=6,unique=False)
    itype=CharField(verbose_name="类型",null=True,max_length=22,unique=False)
    c_time=DateField(verbose_name="创建时间",null=True)
    l_time=DateField(verbose_name="最后时间",null=True)
    isok = DateField(verbose_name="可用", null=True)
    other=CharField(verbose_name="",null=True,unique=False)
    pass
    class Meta:
        database=proxydb

class tb_http_p(Model):
    itype=CharField(verbose_name="",null=False,max_length=32,unique=False)
    url=CharField(verbose_name="URL",null=False,max_length=255,unique=True)
    port=CharField(verbose_name="端口",null=False,max_length=6,unique=False)
    user=CharField(verbose_name="",null=False,max_length=32,unique=False)
    pasd=CharField(verbose_name="",null=False,max_length=32,unique=False)
    c_time=DateField(verbose_name="创建时间",null=True)
    l_time=DateField(verbose_name="最后时间",null=True)
    isok = DateField(verbose_name="可用", null=True)
    other = CharField(verbose_name="", null=True, unique=False)
    class Meta:
        database=proxydb

class tb_sso_p(Model):
    src=CharField(null=True,verbose_name="",unique=False)
    itype=CharField(null=True,verbose_name="",unique=True)
    key=CharField(null=True,verbose_name="",unique=True)
    json=CharField(null=True,verbose_name="",unique=True)
    otherconf=CharField(null=True,verbose_name="",unique=True)
    c_time=DateField(verbose_name="创建时间",null=True)
    l_time=DateField(verbose_name="最后时间",null=True)
    isok=DateField(verbose_name="可用",null=True)
    other = CharField(verbose_name="", null=True, unique=False)
    class Meta:
        database=proxydb

def connects(dbss):
    class connect(Model):
        class   Meta:
            try:
                database=dbss
                database.connect()
            except:
                pass

def closes(dbss):
    class closes(Model):
        class Meta:
            try:
                database=dbss
                database.close()
            except:
                pass

try:tb_http_p.create_table()
except:pass
try:tb_ip_p.create_table()
except:pass
try:tb_sso_p.create_table()
except:pass


def update_check_ip_t(iplist):
    #数据检查修改，读入列表  并比对插入
    bdict = tb_ip_p.select(tb_ip_p.ipport)#查询 获取数据

    list_ipport=[]
    for temp_f_i in iplist:
        if temp_f_i:list_ipport.append(temp_f_i[0])
    # print("iplist is :",list_ipport)

    temp_i=0
    for i in bdict:
        # print(i.ipport)
        # if i in iplist:
        if str(i.ipport) in list_ipport:
            try:
                t=tb_ip_p.update(isok="1").where(tb_ip_p.ipport ==  i.ipport).execute()
                temp_i=temp_i+1
            except:
                print("update err")
                pass
            # print("updata is ok ",i.ipport)
        else:
            t=tb_ip_p.update(isok="0").where(tb_ip_p.ipport ==  i.ipport).execute()
        # t.save()
    print("update_check ok insert is ",temp_i)



def insert_ip_t(ix):
    #插入数据库 ，如果是字典，直接插入单条数据，如果是list 提取字典插入
    # print(type(ix))
    temp_i=0
    if isinstance(ix, list):
        for i in ix:
            if isinstance(i, dict):
                tdict={}
                y=dict(tdict,**i)
                try:
                    x = tb_ip_p.create(**y)
                    x.save()  # ????????buyao?
                    # print("insert ok -",i)
                    temp_i=temp_i+1
                except Exception as b:
                    pass
                    # print(b)
            else:
                # print(i)
                print("Err _INSERT_IP_T 1 type Err")
    elif isinstance(ix,dict):
        try:
            x = tb_ip_p.create(**ix)
            x.save()  # ????????buyao?
            temp_i=temp_i+1
        except Exception as b:
            pass
            # print(b)
    else:
        print(ix)
        print("Err _INSERT_IP_T 2 type Err")
    print("insert ip complete is :",temp_i)

def insert_compay_t(newdict):
    company_tb.create(**newdict)  # 写入数据库
    return "compay_tb table insert complete"

def insert_opsition_t(newdict):
    position.create(**newdict)
    return "position table insert complete"

def insert_txErrsor_t(newdict):
    txErrsor.create(**newdict)
    return "txErrsor table insert complete"


def find_compay_t():
    temp_req=company_tb.select()
    return temp_req

def find_position_t():
    temp_req=position.select()
    return temp_req

def find_ispass_ip_t(isok="1"):
    #------return --list--[ipport type]
    #查找上次标记可以使用的ip
    temp_d_ip=tb_ip_p.select().where(tb_ip_p.isok==isok)
    # temp_d_ip=tb_ip_p.select().where(tb_ip_p.isok==isok)
    return_ip_list=[]
    for i  in temp_d_ip:
        return_ip_list.append([i.ipport,i.itype])
    return return_ip_list

def find_ip_t():
    temp_d_ip=tb_ip_p.select()
    return temp_d_ip
if __name__ == '__main__':
    pass


