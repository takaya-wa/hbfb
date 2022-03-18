from hbfb.arduino_interface import ArduinoInterface

class ArduinoInterface(ArduinoInterface):
    """
    デジタル出力センサー用,任意波形生成
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
            params:[vol1(int), vol2(int)...] (arduino.ver4.actuatorではパラメータは3つ)

        [output]
            "on_time, off_time"
        """
        delay_time = str(goal_ibi/2)
        cmd = delay_time
        for v in params:
            cmd += "," + str(v)
        return cmd

    def stop_cmd(self):
        self.make_cmd(100, [0, 0, 0])