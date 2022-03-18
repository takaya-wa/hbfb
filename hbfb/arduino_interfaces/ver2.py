from hbfb.arduino_interface import ArduinoInterface

class ArduinoInterface(ArduinoInterface):
    """
    デジタル出力センサー用,パルス波生成
    """
    ibi_calc = False
    
    def convert_data(self, data):
        """
        [input]
            data:[ibi(string)...]

        [output]
            [ibi(int) ...]
        """
        return list(map(int, data))

    def make_cmd(self, goal_ibi, params):
        """
        [input]
            goal_ibi:int
            params:[ibi_rate(int)]

        [output]
            "on_time, off_time"
        """
        ontime = goal_ibi * params[0]
        offtime = goal_ibi - ontime

        return str(ontime) + "," + str(offtime)