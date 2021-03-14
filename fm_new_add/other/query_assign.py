import pymysql
from con_db.con_db import db_change


def query_assign(db,device_order_id,assign_profit_status,device_sn):
    print('核对具体分成金额...')
    conn = db_change(db)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        sql = '''SELECT assign_target_id,CAST(origin_ratio AS CHAR ) AS origin_ratio,CAST(assign_ratio AS CHAR ) AS assign_ratio,
         CAST(assign_amount AS CHAR ) AS assign_amount,assign_type FROM `fm_zd_assign_money_log`WHERE device_log_id = '%s' ''' % (device_order_id)
        cursor.execute(sql)
        data_result = cursor.fetchall()
        count_1 = len(data_result)
        print('分润查询结果：',data_result)
    except Exception as e:
        print('查询分润出错，原因：',e)
        count_1 = 0
    cursor.close()
    conn.close()
    if count_1 ==0:
        assign_money_log_list = ['查询分润出错,或者没有找到对应记录']
        pass
    else:
        assign_money_log_list = data_result

    if assign_profit_status == 1:
        conn = db_change(db)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            sql01 = '''SELECT assign_target_id,assign_source_id,CAST(pay_amount AS CHAR) AS pay_amount,CAST(assign_ratio AS CHAR) 
            AS assign_ratio,CAST(assign_amount AS CHAR) AS assign_amount ,assign_type FROM `fm_zd_lianc_profit_log`WHERE 
            device_log_id = '%s' ''' % (device_order_id)
            cursor.execute(sql01)
            result1 = cursor.fetchall()
            count = len(result1)
            print('查询联创收益分成',result1)
        except Exception as e:
            print('分成查询失败，原因',e)
            count = 0
        cursor.close()
        conn.close()
        if count == 0:
            lianc_profit_log_list = ['查询失败或者没有找到对应记录']
        else:
            lianc_profit_log_list = result1
    else:
        lianc_profit_log_list = ['不需要联创分成']

    return assign_money_log_list, lianc_profit_log_list