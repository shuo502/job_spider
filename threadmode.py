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
@file: threadmode.py
@time: 2018/1/31 13:05
"""
import threading as td

def tasks(taskNo=1,target=None,argslist=None):
    print("tasks is run. threading and task is :",taskNo,len(argslist))
    # 传入任务列表，传入使用线程数量，传入运行函数，传入函数参数
    # tasklist = None
    lists=argslist

    def task(target=None, args=None):
        global thread_task_list
        # for i in range(taskNo):
        thread_task = td.Thread(target=target, args=args)
        # thread_task = run(lists.pop(0))  # 初始化线程执行函数 给函数传入参数
        thread_task.start()  # 开始任务
        thread_task_list.append(thread_task)  # 压入线程列表

    global thread_task_list,thread_res_list
    if len(lists)==0:return "Err"
    if target==None:return "Err"
    while 1:#任务空退出
        if len(lists)==0 and len(thread_task_list)==0:#线程空， 列表空退出
            break
        if len(thread_task_list)==0 and lists: #线程空，列表有数据
            if taskNo>len(lists):taskNo=len(lists)
            for _ in range(taskNo):
                t=lists.pop(0)
                if isinstance(t, tuple):
                    args=t
                else:
                    args=(t,)
                task(target=target, args=args)
                #有多余的线程运行任务 初始化启动

        # for i in range(taskNo):#线程循环检查         是否有结束的
        for j in thread_task_list:
            if j.isAlive()==False:#线程停止结束状态

                # print("end is ",j )  # 队列删除一个完成的#
                thread_task_list.remove(j)

                if lists and taskNo>len(thread_task_list):  # 任务列表如果还存在任务。
                    t = lists.pop(0)
                    if isinstance(t, tuple):
                        args = t
                    else:
                        args = (t,)
                    task( target=target, args=args)
                    break#检查一个：
    print("tasks run complete!!")


thread_task_list = []#全局线程池
thread_res_list=[]
src_task_lock=td.Lock()#全局锁
src=""
ilist=["http://baidu.com","http://youku.com","https://github.com"]
if __name__ == '__main__':

    pass
    def runs(url=None):
        # if src_task_lock.acquire():#锁
        #     print("xxxxxxxxxxxxxxxxxxxxxxx")
        #     src_task_lock.release()  # 解锁
        print(url)
        global thread_res_list
        import requests
        res=requests.get(url).content
        thread_res_list.append(res)
        # return res

    import time
    t1=time.time()
    # tasks(taskNo=2,target=runs,argslist=ilist)#input argslist=[(),],taskNo=2,target=runs
    # t2=time.time()
    # print(t2-t1)
    # # print(thread_res_list)
    # for i in thread_res_list:
    #     print([i])
    # tasks(taskNo=3,t)