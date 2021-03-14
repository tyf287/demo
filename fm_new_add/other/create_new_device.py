import time
from con_db.con_db import db_change
from other.time_change import get_local_time_stamp, stamp_to_str


def create_new_device(db,s_uid,agent_id,lianc_id,promote_uid,product_id,device_type,count,name,agent_type):

    sn             = get_local_time_stamp(int(device_type), int(count))
    device_sn_list = []
    for i in sn:
        conn   = db_change(db)
        cursor = conn.cursor()
        try:
            t         = time.time()
            now_t     = stamp_to_str(t)
            device_sn = name + str(i)
            add_sql = '''INSERT INTO fm_zd_shop_device_box (`product_id`, `agent_id`, `lianc_id`, `promote_uid`, `type`,
                                    `device_name`, `slot`, `device_sn`,`status`, `is_outline`,`create_time`,`origin_env`,`delivery_time`)
                                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            product_id  = product_id
            agent_id    = agent_id
            lianc_id    = lianc_id
            promote_uid = promote_uid
            type        = device_type
            device_name = device_sn
            slot        = 7
            device_sn   = device_sn
            status      = 1
            is_outline  = 2
            create_time = now_t
            origin_env  = 32
            delivery_time = now_t

            insert_val  = (product_id, agent_id, lianc_id, promote_uid, type, device_name, slot, device_sn, status, is_outline,
                          create_time, origin_env, delivery_time)
            # print('add_sql:',insert_val)
            cursor.execute(add_sql, insert_val)
            box_id      = conn.insert_id()
            conn.commit()
            re          = box_id
            print('re:',re)
            pass
        except Exception as e:
            print('执行新建设备插入box表出错，原因：', e)
            re = 0
        conn.close()
        if re == 0:
            pass
        else:
            try:
                t       = time.time()
                now_t   = stamp_to_str(t)
                conn    = db_change(db)
                cursor  = conn.cursor()
                add_tran_sql = '''INSERT INTO `fm_zd_device_transfer_log`(`device_sn`, `owner_id`, `owner_type`, `recipient_id`,
                                            `recipient_type`, `operator_id`, `operator_name`,`create_at`, `in_at`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                device_sn    = device_sn
                owner_id     = s_uid
                owner_type   = agent_type
                recipient_id = s_uid
                if agent_type == 1 or agent_type == 2:
                    recipient_type = 1
                else:
                    recipient_type = 4
                recipient_type = recipient_type
                operator_id    = 0
                operator_name  = '总平台发放'
                create_at      = now_t
                in_at          = now_t

                insert_tran_val = (device_sn, owner_id, owner_type, recipient_id, recipient_type, operator_id, operator_name,
                                    create_at, in_at)
                # print('插入划拨表sql:', add_tran_sql)
                cursor.execute(add_tran_sql, insert_tran_val)
                tran_id        = conn.insert_id()
                conn.commit()
                s              = tran_id
                print('s=>', s)
            except Exception as e:
                print('设备插入划拨表失败，原因：', e)
                s = 0
            conn.close()
            if s == 0:
                pass
            else:
                if int(device_type) == 1:
                    conn   = db_change(db)
                    cursor = conn.cursor()
                    val    = []
                    try:
                        add_slot_sql = '''INSERT INTO `fm_zd_shop_device_box_slot`(`box_id`,`device_sn`,`slot`,`create_time`) 
                                            VALUES (%s,%s,%s,%s)'''
                        for i in range(1, 8):
                            box_id      = box_id
                            device_sn   = device_sn
                            slot        = i
                            create_time = now_t
                            insert_slot_val = (box_id, device_sn, slot, create_time)
                            val.append(insert_slot_val)
                        # print('val:', val)
                        cursor.executemany(add_slot_sql, val)
                        conn.commit()
                        print('插入slot完毕')
                    except Exception as e:
                        print('插入【slot】表出错，原因：', e)
                    conn.close()
            device_sn_dic = {}
            device_sn_dic["device_sn"] = device_sn
            if int(device_type) ==1:
                device_sn_dic["device_type"] = '充电宝'
            elif int(device_type) ==2:
                device_sn_dic["device_type"] = '充电线'
            elif int(device_type) ==3:
                device_sn_dic["device_type"] = '自动售货柜'
            device_sn_dic["db"]              = db
            device_sn_dic["create_time"]     = create_time
            device_sn_dic["s_uid"]       = s_uid
            device_sn_list.append(device_sn_dic)
                    # print('新建设备结束')
    # print('device_sn_list:',device_sn_list)
    return device_sn_list

if __name__ == '__main__':
    db          = 'test'
    s_uid       = 3524
    agent_id    = 3524
    lianc_id    = 0
    promote_uid = 0
    product_id  =27
    device_type = 1
    count       = 1
    name        = 'tyf'
    agent_type  = 1
    create_new_device(db,s_uid,agent_id,lianc_id,promote_uid,product_id,device_type,count,name,agent_type)