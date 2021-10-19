import requests
import base64
import json

Email = ""
Apikey = ""
search = ""
page = 1 # 翻页数，默认为第一页
size = 100 # 每次查询返回记录数，默认为100条，最大可设置为10000条 (body字段包含内容较多，建议每次获取≤100条)
fields = "ip"
#【可选参数】字段列表，默认为host，用逗号分隔多个参数，如(fields=ip,title)，
# 可选的列表有：host title ip domain port country province city country_name header server protocol banner cert isp as_
# number as_organization latitude longitude structinfo icp fid

try:
    url = "https://fofa.so/api/v1/search/all?email=%s&key=%s&qbase64=%s&page=%s&size=%s&fields=%s" %(Email, Apikey, str(base64.b64encode(search.encode("utf-8")), "utf-8"),
                                                                                                     page, size, fields)
    res = requests.get(url=url)
    data = json.loads(res.text)
    for ip in data['results']:
        print(ip)
except Exception as e:
    print(e)
