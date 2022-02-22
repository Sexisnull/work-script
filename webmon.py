# -*- coding:utf-8 -*-
# python2
# 网站状态查询脚本

import pycurl

URL = "https://www.baidu.com"
c = pycurl.Curl()
c.setopt(pycurl.URL, URL)
c.setopt(pycurl.CONNECTTIMEOUT, 5) #定义请求连接等待时间
c.setopt(pycurl.TIMEOUT, 5) #定义请求超时时间
c.setopt(pycurl.FORBID_REUSE, 1) #完成交互后断开连接不重用
c.setopt(pycurl.MAXREDIRS, 1) #指定http重定向最大次数
try:
    c.perform()
except Exception,e:
    print "connecion error:"+str(e)
    c.close()

NAMELOOKUP_TIME = c.getinfo(c.NAMELOOKUP_TIME) #获取DNS解析时间
CONNECT_TIME = c.getinfo(c.CONNECT_TIME) #获取建立连接时间
PRETRANSFER_TIME = c.getinfo(c.PRETRANSFER_TIME) #获取从建立连接到准备传输所消耗的时间
STRAR_TIME = c.getinfo(c.STARTTRANSFER_TIME) #获取从建立连接到传输开始的时间
TOTAL_TIME = c.getinfo(c.TOTAL_TIME) #获取传输总时间
HTTP_CODE = c.getinfo(c.HTTP_CODE)
SIZE_DOWNLOAD = c.getinfo(c.SIZE_DOWNLOAD) #获取下载数据包大小
HEADER_SIZE = c.getinfo(c.HEADER_SIZE) #获取http头部大小
SPEED_DOWNLOAD = c.getinfo(c.SPEED_DOWNLOAD) #平均下载速度

print "http状态码：%s" %(HTTP_CODE)
print "DNS解析时间：%.2f ms" %(NAMELOOKUP_TIME*1000)
print "建立连接时间：%.2f ms" %(CONNECT_TIME*1000)
print "准备传输时间：%.2f ms" %(PRETRANSFER_TIME*1000)
print "传输开始时间：%.2f ms" %(STRAR_TIME*1000)
print "传输结束总时间：%.2f ms" %(TOTAL_TIME*1000)
print "下载数据包大小：%d bytes/s" %(SIZE_DOWNLOAD)
print "HTTP头部大小：%d byte" %(HEADER_SIZE)
print "平局下载速度： %d bytes/s" %(SPEED_DOWNLOAD)

c.close()
