import numpy as np

class Action_space():
    def __init__(self, low, high):
        self.low = np.array([low], np.float32)
        self.high = np.array([high], np.float32)

def get_data(ser):
    data = ser.read_all()
    return data.decode().rstrip('\r\n').split('\r\n')

def send_cmd(ser, command):    
    if not ser.isOpen():
        ser.open()

    ser.write(bytes(str(command), encoding='ascii')) # str(param) + 'a'
    ser.flush()

def clip(l, params_info):
    cliped_l = []
    for v, each_info in zip(l, params_info):
        min = each_info[0]
        max = each_info[1]
        if min > v:
            cliped_l.append(min)
        elif max < v:
            cliped_l.append(max)
        else:
            cliped_l.append(v)
    return cliped_l

def params_info_to_min_max_list(params_info):
    min = []
    max = []
    for each_info in params_info:
        min.append(each_info[0])
        max.append(each_info[1])
    return min, max
