#! python3
#! 脚本用于处理企查查导出的数据，并提取到数据库

import openpyxl
import pymysql
from urllib.parse import urlparse


class ReadExcel(object): #读取excel数据的类
    def __init__(self, file_name, sheet_name):
        """
        这个是用来初始化读取对象的
        :param file_name: 文件名 ---> str类型
        :param sheet_name: 表单名 ———> str类型
        """
        # 打开文件
        self.wb = openpyxl.load_workbook(file_name)
        # 选择表单
        self.sh = self.wb[sheet_name]
        self.db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='root',
                                  database='info_abc')


    def read_data_line(self):
        # 按行读取数据转化为列表
        rows_data = list(self.sh.rows)[2:]
        # 获取表单的表头信息
        for i in range(0, len(rows_data)):
            company = rows_data[i][0].value
            district = rows_data[i][6].value
            email1 = rows_data[i][11].value
            email2 = rows_data[i][12].value
            url = rows_data[i][22].value
            domain = urlparse(url).netloc
            email = email1 + '; ' + email2
            sql = "INSERT INTO qichacha_format(company, district, email, url, domain) VALUES ('%s','%s','%s','%s','%s')" % (company, district, email, url, domain)
            self.insertsql(sql)
            print(company)
        self.db.close()

    def insertsql(self, sql):
        cursor = self.db.cursor()
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            self.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()

if __name__ == '__main__':
    r = ReadExcel('69361658.xlsx','1')
    r.read_data_line()
