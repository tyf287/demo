import math
import random
import time

from con_db.con_db import db_change
from other.time_change import str_to_stamp, change_other_time, stamp_to_str


def create_power_order(db,max_day_money,agent_id,shop_manage_id, agent_type, dealer_uid, partner_id, uid, shop_rent_price,
        price_type, lock_shop_id, device_type,box_device_sn, start_time, end_time):
    ttt       = time.time()
    deal_time = stamp_to_str(ttt)
    # print('处理时间：',deal_time)
    start_stamp = str_to_stamp(start_time)
    end_stamp   = str_to_stamp(end_time)
    use_time    = (end_stamp - start_stamp)   # ---得到（单位：秒）的用时
    fen_time    = (end_stamp - start_stamp) / 60 # ---得到（单位：分）的用时
    # print('分为单位的耗时:',fen_time)
    max_money = float(max_day_money)
    msg_list = []
    detail_list = []
    detial_dic  = {}
    if price_type ==1:  #----1小时计费
        if fen_time <= 5:
            total_amount = 0
        elif 5 < fen_time <= 1440:
            total_amount = shop_rent_price*math.ceil(fen_time/60) #---向上取整，获取订单金额---
            if total_amount >= max_money:
                total_amount = max_money
            else:
                total_amount = total_amount
        else:#---此处计算超过一天的计费时间---
            day = fen_time//1440              #---获取整天数
            get_fen_time = fen_time % 1440    #---获取剩余时间数（分钟）
            get_total_amount = float(shop_rent_price*math.ceil(get_fen_time/60)) #---向上取整，获取剩余订单金额---
            if get_total_amount <= max_money:
                total_amount = day * max_money + get_total_amount
            else:
                total_amount = day * max_money + max_money
    else:  #---半小时计费------
        if fen_time <= 5:
            total_amount = 0
        elif 5 < fen_time <= 1440:
            total_amount = float(shop_rent_price*math.ceil(fen_time/30)) #---向上取整，获取订单金额---
            if total_amount >= max_money:
                total_amount = max_money
            else:
                total_amount = total_amount
        else:#---此处计算超过一天的计费时间---
            day = fen_time//1440              #---获取整天数
            get_fen_time = fen_time % 1440    #---获取剩余时间数（分钟）
            get_total_amount = float(shop_rent_price*math.ceil(get_fen_time/30)) #---向上取整，获取剩余订单金额---
            if get_total_amount <= max_money:
                total_amount = day * max_money + get_total_amount
            else:
                total_amount = day * max_money + max_money
    # print('订单应支付金额:',total_amount)
    # exit(0)
    tt        = change_other_time(start_time)
    ordertime = tt[0]
    deviceordertime = tt[1]
    conn   = db_change(db)
    cursor = conn.cursor()
    try:
        insert_sql = '''INSERT INTO `fm_zd_device_use_log`(`agent_id`, `shop_manage_id`,`agent_type`,  `dealer_uid`, `partner_id`,`uid`,
                             `order_id`, `order_sn`, `device_order_sn`, `shop_rent_price`, `price_type`, `lock_shop_id`, `rent_shop_id`,
                             `device_type`,`slot`, `box_device_sn`, `device_sn`, `total_amount`, `pay_amount`,`pay_type`,`deal_status`, `deduct_status`,
                              `device_status`,`start_time`, `end_time`, `use_time`, `is_assign`,`create_time`) VALUES 
                              (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
        # print('insert_sql:',insert_sql)
        agent_id        = agent_id
        shop_manage_id  = shop_manage_id
        agent_type      = agent_type
        dealer_uid      = dealer_uid
        partner_id      = partner_id
        uid             = uid
        order_id        = '123456'
        order_sn        = ordertime
        device_order_sn = deviceordertime
        shop_rent_price = shop_rent_price
        price_type      = price_type
        lock_shop_id    = lock_shop_id
        rent_shop_id    = lock_shop_id
        device_type     = device_type
        slot            = random.randint(1, 7)
        box_device_sn   = box_device_sn
        device_sn       = box_device_sn
        deal_status     = 1
        pay_type        = 1
        deduct_status   = 1
        device_status   = 2
        start_time      = start_time
        end_time        = end_time
        use_time        = use_time
        total_amount    = total_amount
        pay_amount      = total_amount
        is_assign       = 2
        create_time     = start_time

        insert_val = (agent_id, shop_manage_id,agent_type, dealer_uid, partner_id, uid, order_id, order_sn, device_order_sn,
                      shop_rent_price,price_type, lock_shop_id, rent_shop_id, device_type, slot, box_device_sn, device_sn,
                      total_amount,pay_amount,pay_type ,deal_status, deduct_status, device_status, start_time, end_time,
                      use_time, is_assign, create_time)

        # print('insert_val:',insert_val)
        cursor.execute(insert_sql, insert_val)
        id = conn.insert_id()
        conn.commit()
        # print('完成订单插入并获得id为：',id)
    except Exception as e:
        print('执行插入【device_use_log】表失败并回滚，原因：', e)
        conn.rollback()
        id = 0
    conn.close()
    # ---------执行插入【order】表------
    if id == 0:
        pass
    else:
        conn   = db_change(db)
        cursor = conn.cursor()
        try:
            insert_order_sql = '''INSERT INTO `fm_zd_order`(`device_log_id`,`shop_id`, `uid`,`order_sn`, `total_amount`,
                                 `pay_amount`, `order_status`,`order_type`,`device_sn`,`end_time`,`create_time`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            device_log_id = id
            shop_id       = lock_shop_id
            uid           =  uid
            order_sn      = order_sn
            total_amount  = total_amount
            pay_amount    = total_amount
            order_status  = 3
            order_type    = 12
            device_sn     = box_device_sn
            end_time      = end_time
            create_time   = start_time

            insert_order_val = (
            device_log_id, shop_id, uid, order_sn, total_amount, pay_amount, order_status,order_type, device_sn, end_time,
            create_time)
            cursor.execute(insert_order_sql, insert_order_val)
            get_order_id = conn.insert_id()
            conn.commit()
            # print('完成【order】表插入并获得id为：',get_order_id)
        except Exception as e:
            print('执行插入【order】表出错并回滚，原因：', e)
            msg = '执行插入【order】表出错并回滚，原因：' + str(e)
            msg_list.append(msg)
            get_order_id = 0
        conn.close()
        if get_order_id == 0:
            pass
        else:
            conn = db_change(db)
            cursor = conn.cursor()
            try:
                update_sql = '''update fm_zd_device_use_log set order_id = %s where id = %s''' % (get_order_id, id)
                cursor.execute(update_sql)
                conn.commit()
            except Exception as e:
                print('执行更新order_id出错，原因：', e)
            conn.close()
        conn   = db_change(db)
        cursor = conn.cursor()
        sql_log = '''INSERT INTO `fm_zd_device_use_log_assign_log`(rent_log_id, device_type, end_time,
            assign_money_status,assign_profit_status,active_device_status) VALUES (%s, %s, %s, %s, %s, %s)'''

        rent_log_id          = id
        device_type          = 1
        end_time             = end_time
        assign_money_status  = 2
        assign_profit_status = 2
        active_device_status = 2

        insert_log_val       = (rent_log_id, device_type, end_time, assign_money_status, assign_profit_status,
                                active_device_status)
        try:
            cursor.execute(sql_log, insert_log_val)
            conn.commit()
            conn.close()
            # print('插入SQL【fm_zd_device_use_log_assign_log】表完毕......')
        except:
            conn.rollback()
            # print('插入SQL【fm_zd_device_use_log_assign_log】表出错，回滚插入')
            conn.close()
        msg_txt         = '创建订单完毕'
        device_txt      = '设备编号为：【'+device_sn+'】'
        device_order_id ='订单<id>为：【'+str(id)+'】'
        dvice_amount    = '订单金额为：【'+str(total_amount)+'】'
        #---
        msg_list.append(msg_txt)
        msg_list.append(device_txt)
        msg_list.append(device_order_id)
        msg_list.append(dvice_amount)
        #---订单详情----
        detial_dic["device_sn"]    = device_sn
        detial_dic["order_id"]     = id
        detial_dic["db"]           = db
        detial_dic["deal_time"]  = deal_time
        detial_dic["total_amount"] = total_amount
        detial_dic["agent_id"]     = agent_id
        detail_list.append(detial_dic)

    return msg_list, id, device_sn,detail_list

if __name__ == '__main__':

    create_power_order(db, max_day_money, agent_id, agent_type, dealer_uid, partner_id, uid, shop_rent_price,
                       price_type, lock_shop_id, device_type, box_device_sn, start_time, end_time)