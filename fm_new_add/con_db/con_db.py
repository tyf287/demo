import pymysql
import time
import sys


def db_change(db):
    if db == 'dev':
        conn = pymysql.connect(
            host='132.232.4.85',
            port=3306,
            user='yf_test',
            passwd='K66sJjcdhKmKrR6G',
            db='yf_test'
        )
        pass
    elif db == 'test':
        conn = pymysql.connect(
            host='122.112.193.206',
            port=3306,
            user='yuanfang',
            passwd='@yuan666fang@',
            db='zhidian_dev'
        )
        pass
    elif db == 'master':
        conn = pymysql.connect(
            host='122.112.193.206',
            port=3306,
            user='yuanfang',
            passwd='@yuan666fang@',
            db='zhidian_master'
        )
        pass
    else:
        print('数据库输入错误，请重新选择')
        conn = 0
        # exit(0)
        pass
    return conn

if __name__ == '__main__':
    db_change('test')
    # def dev_change():
    #     while True:
    #         try:
    #             conn_dev = pymysql.connect(
    #                 host='132.232.4.85',
    #                 port=3306,
    #                 user='yf_test',
    #                 passwd='K66sJjcdhKmKrR6G',
    #                 db='yf_test'
    #             )
    #             break
    #         except Exception as e:
    #             print('数据库连接失败，原因：',e)
    #             time.sleep(3)
    #     return conn_dev
    #
    # def test_change():
    #     while True:
    #         try:
    #             conn_test = pymysql.connect(
    #                 host='122.112.193.206',
    #                 port=3306,
    #                 user='yuanfang',
    #                 passwd='@yuan666fang@',
    #                 db='zhidian_dev'
    #             )
    #             break
    #         except Exception as e:
    #             print('数据库连接失败，原因：', e)
    #             time.sleep(3)
    #     return conn_test
    #
    # def master_change():
    #     while True:
    #         try:
    #             conn_master = pymysql.connect(
    #                 host='122.112.193.206',
    #                 port=3306,
    #                 user='yuanfang',
    #                 passwd='@yuan666fang@',
    #                 db='zhidian_master'
    #             )
    #             break
    #         except Exception as e:
    #             print('数据库连接失败，原因：',e)
    #             time.sleep(3)
    #     return conn_master

