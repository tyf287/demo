import time
import pymysql
from django.shortcuts import render
from con_db.con_db import db_change
from other.create_new_device import create_new_device
from other.cteate_power_order import create_power_order
from other.query_assign import query_assign
from other.query_remarks import query_remarks
from other.time_change import stamp_to_str, str_to_stamp


def device(request):
    name_dic         = {}
    name         = request.POST.get('device_first_name')
    count        = request.POST.get('add_acount')
    device_type  = request.POST.get('device_type')
    agent_mobile = request.POST.get('mobile')
    agent_type   = request.POST.get('agent_type')
    product_id   = request.POST.get('device_sn_id')
    db           = request.POST.get('db_change')

    # print('前端获得设备前置名：', name)
    # print('前端获得新增设备数量：', count)
    # print('数据库选择为：',db,type(db))

    # --------先查询服务商-----------------------
    # print('agent_mobile:',agent_mobile)
    if name ==None or count ==None or agent_mobile ==None:
        pass
    else:
        conn = db_change(db)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            agent_sql = '''select id,is_agent,is_promote,is_lianc from fm_zd_user where mobile = %s''' % (agent_mobile)
            cursor.execute(agent_sql)
            result = cursor.fetchall()
            re = len(result)
            # print('re:',re)
            pass
        except Exception as e:
            print('查询服务商信息出错，原因：', e)
            re = 0
        conn.close()
        if re == 0:
            # print('没有查找到该服务商信息，请检查')
            name_dic["txt"] = [{'error':'没有找到服务商【' + agent_mobile + '】的信息，请检查'}]
            pass
        else:
            s_uid = result[0]["id"]
            is_agent = result[0]["is_agent"]
            is_promote = result[0]["is_promote"]
            is_lianc = result[0]["is_lianc"]
            if int(agent_type) == 1:
                agent_count = 1
                agent_id = s_uid
                lianc_id = 0
                promote_uid = 0
                if agent_count != is_agent:
                    sss = 0
                else:
                    sss = 1
            elif int(agent_type) == 2:
                promte_count = 1
                agent_id = 0
                lianc_id = 0
                promote_uid = s_uid
                if promte_count != is_promote:
                    sss = 0
                else:
                    sss = 1
            elif int(agent_type) == 3:
                lianc_count = 1
                agent_id = 0
                lianc_id = s_uid
                promote_uid = 0
                if lianc_count != is_lianc:
                    sss = 0
                else:
                    sss = 1
            else:
                print('服务商类型输错，请检查')
                sss = 0
            if sss == 0:
                # print('没有找到服务商【' + agent_mobile + '】的类型或者【类型输错】，请检查')
                name_dic["txt"] = [{'error':'没有找到服务商【' + agent_mobile + '】的类型-或者-【类型输错】，请检查'}]
                pass
            else:
                # print('device_type:',device_type,type(device_type))
                # print('count:',count,type(count))
                result_val = create_new_device(db, s_uid, agent_id, lianc_id, promote_uid, product_id, device_type,
                                               count, name, agent_type)
                name_dic["txt"] = result_val
                print('result_val:',result_val)
    print('name_dic:',name_dic)
    return render(request, 'device.html', name_dic)

def show(request):
    txt = {}
    return render(request, 'device.html')

def order(request):
    txt = {}
    rent_mobile   = request.POST.get('rent_mobile')     #----租借充电宝/购买商品 用户id----
    box_device_sn = request.POST.get('box_device_sn')  #----设备编号----
    start_time    = request.POST.get('start_time')     #----租借充电宝/购买商品 开始时间----
    rent_time     = request.POST.get('rent_time')      #----租借充电宝/购买商品 耗时---
    end_time      = request.POST.get('end_time')       #----租借充电宝 结束时间---（选择购买商品，此处不需要购买）-
    db            = request.POST.get('db_change')
    #-------查询对应设备的服务商，经销商，合伙人，以及店铺信息-------
    if rent_mobile==None or box_device_sn ==None:
        txt["detail"] = [{'error':'租借用户或者设备编号不能为空'}]
        pass
    else:
        conn = db_change(db)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            rent_sql = '''select id from fm_zd_user where mobile = %s''' % (rent_mobile)
            cursor.execute(rent_sql)
            result = cursor.fetchall()
            rent_txt = len(result)
            rent_uid = result[0]["id"]
            # print('re:',re)
        except Exception as e:
            print('查询服务商信息出错，原因：', e)
            rent_txt = 0
        conn.close()
        if rent_txt ==0:
            txt["detail"] = [{'error': '租借用户不存在'}]
            pass
        else:
            conn   = db_change(db)
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            try:
                device_sn_sql = '''select agent_id,lianc_id,promote_uid,shop_id,partner_id,dealer_uid,type from fm_zd_shop_device_box
                                    where device_sn = %s'''%("'"+box_device_sn+"'")
                cursor.execute(device_sn_sql)
                result = cursor.fetchall()
                re     = len(result)
            except Exception as e:
                print('查询设备对应服务商信息失败，原因：',e)
                re = 0
            conn.close()
            if re == 0:
                txt["detail"] = [{'error': '没有找到设备【'+str(box_device_sn)+'】对应信息，请检查是否存在该设备'}]
                pass
            else:
                agent_id    = result[0]["agent_id"]
                lianc_id    = result[0]["lianc_id"]
                promote_uid = result[0]["promote_uid"]
                shop_id     = result[0]["shop_id"]
                partner_id  = result[0]["partner_id"]
                dealer_uid  = result[0]["dealer_uid"]
                device_type = result[0]["type"]
                if agent_id > 0 and lianc_id == 0 and promote_uid == 0:
                    agent_id   = agent_id
                    agent_type = 1
                elif agent_id == 0 and lianc_id > 0 and promote_uid == 0:
                    agent_id   = lianc_id
                    agent_type = 3
                elif agent_id == 0 and lianc_id == 0 and promote_uid > 0:
                    agent_id   = promote_uid
                    agent_type = 2
                else:
                    agent_id   = 0
                    agent_type = 0
                    msg        = '该设备暂未绑定任何服务商，请检查'
                    exit(0)
                if shop_id == 0:
                    txt["detail"] = [{'error': '该设备【' + str(box_device_sn) + '】暂未绑定店铺，请检查'}]
                else:
                    if device_type == 3:
                        print('此为自动售货柜')
                    else:
                        #----------【查询，店铺信息，租借单价，最高封顶金额】-----
                        if len(start_time) ==0:
                            txt["detail"] = [{'error': '必须传入订单开始时间！'}]
                            pass
                        else:
                            if len(end_time) > 0:
                                end_time = end_time
                            else:
                                usetime  = float(rent_time) * 60 * 60  # ----转换成单位：秒---
                                end_time = stamp_to_str(str_to_stamp(start_time) + usetime)
                            conn   = db_change(db)
                            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
                            try:
                                query_shop_sql = '''select shop_manage_id,max_day_money,price_type,fee_ratio from fm_zd_shop where id = %s''' %(shop_id)
                                cursor.execute(query_shop_sql)
                                query_shop_result = cursor.fetchall()
                                query_shop_msg    = len(query_shop_result)
                            except Exception as e:
                                print('查询店铺信息失败，原因：',e)
                                query_shop_msg = 0
                            conn.close()
                            if query_shop_msg == 0:
                                print('店铺信息查询失败，请检查，店铺是否存在')
                                txt["detail"] = [{'error': '店铺信息查询失败，请检查，店铺是否存在'}]
                                pass
                            else:
                                max_day_money  = query_shop_result[0]["max_day_money"]
                                price_type     = query_shop_result[0]["price_type"]
                                fee_ratio      = query_shop_result[0]["fee_ratio"]
                                shop_manage_id = query_shop_result[0]["shop_manage_id"]

                            #-----------【插入订单】--------------------------
                                uid = rent_uid
                                result_order = create_power_order(db, max_day_money, agent_id,shop_manage_id, agent_type, dealer_uid, partner_id, uid, fee_ratio,
                                   price_type, shop_id, device_type, box_device_sn, start_time, end_time)
                                # txt["msg"]      = result_order[0]
                                device_order_id = result_order[1]
                                device_sn       = result_order[2]
                                txt['detail']      = result_order[3]
                                # print('detail:',result_order[3])
                                # print('result_order',result_order)
                                result_remarks = query_remarks(db,device_order_id,agent_type)
                                # print('分成最后结果：',result_remarks)
                                message         = result_remarks[0]
                                assign_profit_status = result_remarks[1]
                                if message == '分润成功' or message == '分成分润，均成功' or message == '分润成功，不需要【联创团队或者推广分成】':
                                    # print('分成结束，开始检测具体分成金额')
                                    assign_result = query_assign(db,device_order_id,assign_profit_status,device_sn)
                                    txt["msg"]   = assign_result[0]
                                    txt["lianc"] = assign_result[1]
                                else:
                                    # print('订单【'+str(device_order_id)+'】,分润分成失败，请检查')
                                    txt['detail'] ={'error':'订单【'+str(device_order_id)+'】,分润分成失败，请检查'}
    # print('分成具体金额：',txt)
    return render(request, 'order.html',txt)
