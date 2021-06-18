# python2
# -*- coding: utf-8 -*-

import requests,time
import json
import logging
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(
    filename='cve-mon.log',
    filemode='a',
    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    )

def getcveNews():
    try:
        api = "https://api.github.com/search/repositories?q=CVE-2021&sort=updated"
        req = requests.get(api).text
        req_jsondata = json.loads(req)
        cve_total_count = req_jsondata['total_count']
        cve_url = req_jsondata['items'][0]['html_url']
        cve_description = req_jsondata['items'][0]['description']
        cve_created_at = req_jsondata['items'][0]['created_at']
        cve_updated_at = req_jsondata['items'][0]['updated_at']
        msg = "漏洞地址：" + str(cve_url).encode('utf-8') + "\n漏洞说明：" + str(cve_description).encode('utf-8') + "\n创建时间：" + str(cve_created_at).encode('utf-8') + "\n更新时间：" + str(cve_updated_at).encode('utf-8')
        return cve_total_count, msg

    except Exception as e:
        logging.error(str(e))


def getcnvdNews():
    try:
        api = "https://api.github.com/search/repositories?q=CNVD-2021&sort=updated"
        req = requests.get(api).text
        req_jsondata = json.loads(req)
        cnvd_total_count = req_jsondata['total_count']
        cnvd_url = req_jsondata['items'][0]['html_url']
        cnvd_description = req_jsondata['items'][0]['description']
        cnvd_created_at = req_jsondata['items'][0]['created_at']
        cnvd_updated_at = req_jsondata['items'][0]['updated_at']
        msg = "漏洞地址：" + str(cnvd_url).encode('utf-8') + "\n漏洞说明：" + str(cnvd_description).encode('utf-8') + "\n创建时间：" + str(cnvd_created_at).encode('utf-8') + "\n更新时间：" + str(cnvd_updated_at).encode('utf-8')
        return cnvd_total_count, msg

    except Exception as e:
        logging.error(str(e))

def sendNews():
    initial_cve_num = 386
    initial_cnvd_num = 16
    qiyeweixin_robot = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' # 企业微信机器人推送
    headers = {'Content-Type': 'application/json'}
    while True:
        senddata = {
            "msgtype": "text",
            "text": {
                "content": ""
            }
        }
        try:
            cve_total_count, msg = getcveNews()
            if cve_total_count != initial_cve_num:
                initial_cve_num = initial_cve_num + 1
                senddata['text']['content'] = msg
                requests.post(url=qiyeweixin_robot, headers=headers, data=json.dumps(senddata))
        except:
            pass
        try:
            cnvd_total_count, msg = getcnvdNews()
            if cnvd_total_count != initial_cnvd_num:
                initial_cnvd_num = initial_cnvd_num + 1
                senddata['text']['content'] = msg
                requests.post(url=qiyeweixin_robot, headers=headers, data=json.dumps(senddata))
        except:
            pass
        time.sleep(300)


if __name__ == '__main__':
    sendNews()
