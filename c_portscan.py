#!/usr/bin/python3
# coding:utf-8
# 批量扫描C段目标tcp端口开放扫描及应用端口banner识别

import sys
import socket
import requests
import time
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing.dummy import Lock
import argparse
import xlwt


def format_target(ips):
    # ip处理
    iplist = []
    for i in range(1, 255):
        iplist.append(ips.split('/')[0][:-1] + str(i))

    return iplist


def format_file(file):
    # ip处理
    iplist = []
    with open(file, 'r') as f:
        for i in f.readlines():
            iplist.append(i)

    return iplist


def scan_poll(target):
    targets = []
    ports = ['21', '22', '23', '53', '67', '68', '69', '80', '81', '82', '88', '135', '139', '143', '161', '389', '443',
             '445', '873', '888', '1090', '1091', '1099', '1433', '1521', '2049', '2181', '3306', '3389', '3690',
             '5000',
             '5001', '5002', '5060', '5061', '5432', '5632', '5900', '6000', '6379', '8443', '8888', '8983', '9200',
             '9300', '50050', '50070', '7000-7100', '8000-8100', '9000-9100', '17000-17100', '18000-18100',
             '19000-19100', '27000-27100', '28000-28100', '29000-29100', ]
    for t in target:
        for p in ports:
            if '-' in p:
                for p2 in range(int(p.split('-')[0]), int(p.split('-')[1]) + 1):
                    targets.append(t + ':' + str(p2))
            else:
                targets.append(t + ':' + p)

    return targets


class Scanner(object):
    def __init__(self, targets, outfile=None):
        self.targets = targets
        self.time = time.time()
        self.result = []
        self.mutex = Lock()
        self.outfile = outfile
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    def scan_port(self, target):
        # 端口扫描
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            return True if s.connect_ex((target.split(':')[0], int(target.split(':')[1]))) == 0 else False
        except Exception as e:
            pass
        finally:
            s.close()

    def get_http_banner(self, url):
        # http/https请求获取banner
        try:
            r = requests.get(url, headers=self.headers,
                             timeout=2, verify=False, allow_redirects=True)
            soup = BeautifulSoup(r.content, 'lxml')
            return r.status_code, soup.title.text.strip('\n').strip()
        except Exception as e:
            pass

    def get_socket_info(self, target):
        # socket获取banner
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)
            s.connect((target.split(':')[0], int(target.split(':')[1])))
            s.send(b'hello\r\n')
            return s.recv(1024).decode().split('\r\n')[0].strip('\r\n')
        except Exception as e:
            pass
        finally:
            s.close()

    def fofa_api():
        pass

    def output_excel(self, data):
        # data = [['ip:port','code','target'],['ip:port','code','target']]
        data = [d for d in data if d != []]
        xl = xlwt.Workbook(encoding='utf-8')
        sheet = xl.add_sheet('one')
        sheet.write(0, 0, 'ip&port')
        sheet.write(0, 1, 'status')
        sheet.write(0, 2, 'banner')
        for l in range(1, len(data) + 1):
            sheet.write(l, 0, data[l - 1][0])
            sheet.write(l, 1, data[l - 1][1])
            sheet.write(l, 2, data[l - 1][2])

        xl.save(self.outfile)

    def run(self, target):
        data = []
        try:
            if self.scan_port(target):
                banner = self.get_http_banner('http://{}'.format(target))
                self.mutex.acquire()
                if banner:
                    print(target + ' open ' + str(banner[0]) + ' ' + banner[1])
                    data.append(target)
                    data.append(banner[0])
                    data.append(banner[1])
                else:
                    banner = self.get_http_banner('https://{}'.format(target))
                    if banner:
                        print(target + ' open ' + str(banner[0]) + ' ' + banner[1])
                        data.append(target)
                        data.append(banner[0])
                        data.append(banner[1])
                    else:
                        banner = self.get_socket_info(target)
                        if banner:
                            print(target + ' open ' + 'xxx' + banner)
                            data.append(target)
                            data.append('xxx')
                            data.append(banner)
                        else:
                            print(target + ' open')
                            data.append(target)
                            data.append('xxx')
                            data.append('unknown')
                self.mutex.release()
        except Exception as e:
            pass
        finally:
            return data

    def start(self):
        try:
            print('-' * 60 + '开始扫描')
            # 线程数, 可根据网络和机器性能调整
            pool = ThreadPool(processes=1000)
            # get传递超时时间，用于捕捉ctrl+c
            data = pool.map_async(self.run, self.targets).get(0xffff)
            pool.close()
            pool.join()
            print('-' * 60+ '扫描完成')
            print('[-] 扫描完成耗时: {} 秒.'.format(time.time() - self.time))
            if self.outfile:
                self.output_excel(data)
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print(self.R + u'\n[-] 用户终止扫描...')
            sys.exit(1)


if __name__ == '__main__':
    banner = """
                                   ██                                     
         ██████                   ░██                                     
  █████ ░██░░░██  ██████  ██████ ██████  ██████  █████   ██████   ███████ 
 ██░░░██░██  ░██ ██░░░░██░░██░░█░░░██░  ██░░░░  ██░░░██ ░░░░░░██ ░░██░░░██
░██  ░░ ░██████ ░██   ░██ ░██ ░   ░██  ░░█████ ░██  ░░   ███████  ░██  ░██
░██   ██░██░░░  ░██   ░██ ░██     ░██   ░░░░░██░██   ██ ██░░░░██  ░██  ░██
░░█████ ░██     ░░██████ ░███     ░░██  ██████ ░░█████ ░░████████ ███  ░██
 ░░░░░  ░░       ░░░░░░  ░░░       ░░  ░░░░░░   ░░░░░   ░░░░░░░░ ░░░   ░░ 

                                                                 --by kid
    """
    print(banner)
    parser = argparse.ArgumentParser(usage='python3 %(prog)s -ip 1.1.1.1')
    parser.add_argument("-ip", dest='ip', help='ipv4 或 ipv6地址')
    parser.add_argument("-cip", dest='cip', help='C段IP')
    parser.add_argument("-f", "--file", dest='file', help='ip地址文件')
    parser.add_argument("-o", "--output", dest='output', help='输出到xls文件')
    parser.add_argument("-so", "--fofa", dest='fofa', help='调用fofaAPI查询')

    args = parser.parse_args()
    iplist = []
    if args.cip:
        iplist = format_target(args.cip)
    if args.file:
        iplist = format_target(args.file)
    if args.ip:
        iplist.append(args.ip)
    if iplist:
        targets = scan_poll(iplist)
        if args.output:
            myscan = Scanner(targets=targets, outfile=args.output)
            myscan.start()
        else:
            myscan = Scanner(targets=targets)
            myscan.start()
    else:
        print('Usage:python3 c_portscan.py -cip 1.1.1.1/24')
