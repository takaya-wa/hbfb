from hbfb.arduino_interface import ArduinoInterface

class ArduinoInterface(ArduinoInterface):
    """
    デジタル出力センサー用,パルス波生成(パラメータ追加)
    """
    ibi_calc = False
    
    def convert_data(self, data):
        """
        [input]
            data:[ibi(string)...]

        [output]
            [ibi(int) ...]
        """
        if data[0]:
            return list(map(int, data))
        else:
            return None

    def make_cmd(self, goal_ibi, params):
        """
        [input]
            goal_ibi:int
            params:[vol(int), pulse_rate(int)]

        [output]
            "on_time, off_time"
        """
        ontime = goal_ibi * params[1] / 100
        offtime = goal_ibi - ontime
        voltage = params[0]

        return str(ontime) + "," + str(offtime) + "," + str(voltage)

    def stop_cmd(self):
        return self.make_cmd(100, [0, 0])