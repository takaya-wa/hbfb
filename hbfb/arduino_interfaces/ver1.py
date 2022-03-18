from hbfb.arduino_interface import ArduinoInterface

class ArduinoInterface(ArduinoInterface):
    """
    アナログ出力センサー用,パルス波生成
    """
    ibi_calc = True

    def convert_data(self, data):
        """
        [input]
            data:[signal, time, ...]

        [output]
            [(signal, time), ...]
        """
        data_list = []

        for signal, t in zip(data[0::2], data[1::2]):
            one_data = (int(signal), int(t))
            data_list.append(one_data)

        return data_list

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