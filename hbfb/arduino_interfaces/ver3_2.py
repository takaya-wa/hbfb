from hbfb.arduino_interface import ArduinoInterface

class ArduinoInterface(ArduinoInterface):
    """
    デジタル出力センサー用,パルス波生成(パラメータ追加)
    """
    ibi_calc = False
    
    def convert_data(self, data):
        """
        [input]
            [ibi(string)...]

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
        ontime = goal_ibi * params["pulse_rate"]
        offtime = goal_ibi - ontime
        voltage = params["vol"]

        return str(ontime) + "," + str(offtime) + "," + str(voltage)

    def stop_cmd(self):
        return self.make_cmd(100, {"vol":0, "pulse_rate":0})