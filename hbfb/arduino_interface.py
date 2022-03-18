from abc import ABCMeta, abstractmethod

class ArduinoInterface(metaclass=ABCMeta):
    ibi_calc = True

    @abstractmethod
    def convert_data():
        raise NotImplementedError()

    @abstractmethod
    def make_cmd():
        raise NotImplementedError()

    @abstractmethod
    def stop_cmd():
        pass