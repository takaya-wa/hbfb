from time import sleep
from importlib import import_module
import statistics

import serial

from hbfb.ibi import Ibi

class Agent:
    def __init__(self, margin=30, extend_num=20, extend=True, data_interface="ver3"):
        """
        """

        data_interface = import_module(f"sync_cycle.data_interfaces.{data_interface}")
        self.data_interface = data_interface.DataInterface() # arduino_interfaceのほうがいいんじゃね？

        self.margin = margin
        self.extend_num = extend_num
        self.extend = extend

        # 要検討
        self.ser_sensor = serial.Serial('COM3', 9600, timeout=0.1) 
        self.ser_actuator = serial.Serial('COM4', 9600, timeout=0.1)

        
        if self.data_interface.ibi_calc:
            self.ibi_calc = Ibi()

        self.reset()
        
    def __repr__(self):
        val = f"ibi:{self.ibi}\ngoal_ibi:{self.goal_ibi}"
        return val
    
    def _get_data(self):
        ser = self.ser_sensor
        sleep(2)
        
        data = ser.read_all()
        return data.decode().rstrip('\r\n').split('\r\n')

    def _send_cmd(self, command):
        ser = self.ser_actuator  
        
        if not ser.isOpen():
            ser.open()

        ser.write(bytes(str(command), encoding='ascii')) # str(param) + 'a'
        ser.flush()

    def observe(self):
        data = None
        while not data:
            data = self._get_data()

        data = self.data_interface.convert_data(data)

        if self.data_interface.ibi_calc:
            ibi_list, error_log = self.ibi_calc.calc_ibi(data)

            if error_log["No signal"]:
                print("シグナルがありません。")
            if error_log["Error"]:
                print("脈拍を検知できません。センサーの装着を再確認してください。") 
        else:
            ibi_list = data

        if ibi_list:
            ibi = statistics.median(ibi_list) #self.ibi どうやって決めるか検討
        else:
            return False

        if 300 < ibi < 1600: #300 < goal_ibi < 1600 まで
            self.ibi = ibi
            return True
        else:
            print("IBIの計算結果に異常があります。")
            return False

    def action(self, params):
        cmd = self.data_interface.make_cmd(self.goal_ibi, params)
        self._send_cmd(cmd)

    def sync_check(self):
        if abs(self.ibi - self.goal_ibi) <= self.margin:
            self.extend_ibi()
            return True
        else:
            return False

    def extend_ibi(self):
        if self.extend:
            self.goal_ibi += self.extend_num
        else:
            self.goal_ibi -= self.extend_num

    def close(self):
        self.ser_sensor.close()
        self.ser_actuator.close()

    def reset(self):
        success = False
        while not success:
            sleep(15)
            success = self.observe()

        self.goal_ibi = self.ibi
        self.extend_ibi()

    def stop(self):
        cmd = self.data_interface.stop_cmd()
        self._send_cmd(cmd)
        self.close()