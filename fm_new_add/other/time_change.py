import random
import time

def str_to_stamp(get_time):
    in_time   = get_time
    timeArray = time.strptime(in_time, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

def stamp_to_str(get_time):
    in_time   = get_time
    timeArray = time.localtime(in_time)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def change_other_time(get_time):
    timeStamp = str_to_stamp(get_time)
    timeArray = time.localtime(timeStamp)
    ordertime = str(time.strftime("%Y%m%d%H%M%S", timeArray)) + str(random.randint(10000000000000, 99999999999999))
    # deviceordertime = str(time.strftime("%Y%m%d%H%M%S", timeArray)) + str(random.randint(10000000000000, 99999999999999))
    deviceordertime = str(time.strftime("%Y%m%d%H%M%S", timeArray))
    return ordertime,deviceordertime

def get_local_time_stamp(device_type,count):
    t         = time.time()
    txt_list  = []
    a         = [i for i in range(1, int(count)+1)]
    if int(device_type) == 1:
        tt    = str(t).split('.')
        for i in a:
            txt = str(tt[0]) + '00' + str(i)
            txt_list.append(txt)
    else:
        timeArray = time.localtime(t)
        ordertime = str(time.strftime("%Y%m%d%H%M%S", timeArray))
        for i in a:
            txt   = str(ordertime)+'00'+str(i)
            txt_list.append(txt)

    return txt_list
if __name__ == '__main__':

    # tt=change_other_time("2013-10-10 23:40:00")
    ttt = get_local_time_stamp(2, 5)
    print(ttt)