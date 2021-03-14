import os
import time
from con_db.con_db import db_change


def query_remarks(db,id,agent_type):
    while True:
        print('开始检查分成结果****')
        conn = db_change(db)
        cursor = conn.cursor()
        log_id = id
        sql1 ='''SELECT assign_money_status,assign_profit_status FROM `fm_zd_device_use_log_assign_log` WHERE rent_log_id = '%s' '''%(log_id)
        # print('sql1=>',sql1)
        cursor.execute(sql1)
        results = cursor.fetchall()[0]
        cursor.close()
        conn.close()
        assign_money_status  = results[0]
        assign_profit_status = results[1]
        if agent_type == 3:
            if assign_money_status != 2 and assign_money_status != 7 and assign_profit_status != 2 and assign_profit_status !=7:
                if assign_money_status == 1:
                    if assign_profit_status == 1:
                        print('分成分润，均成功')
                        results_txt = '分成分润，均成功'
                    elif assign_profit_status == 3:
                        print('不需要【联创团队或者推广分成】')
                        results_txt = '分润成功，不需要【联创团队或者推广分成】'
                    elif assign_profit_status == 4:
                        print('分成失败')
                        results_txt = '分润成功，分成失败'
                else:
                    print('分润失败')
                    results_txt = '分润失败'
                break
            else:
                time.sleep(2)
        else:
            print('检查分成结果=》', results)
            if assign_money_status != 2 and assign_money_status != 7:
                if assign_money_status ==1:
                    print('分润成功')
                    results_txt = '分润成功'
                else:
                    print('分润失败')
                    results_txt = ['分润失败']
                break
            else:
                time.sleep(2)
    return results_txt, assign_profit_status

if __name__ == '__main__':
    query_remarks()