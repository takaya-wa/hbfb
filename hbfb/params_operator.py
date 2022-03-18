from abc import ABCMeta, abstractmethod

class ParamsOperator(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, params, params_info):
        self.sync = False
        self.params = params
        self.params_info = params_info

    @abstractmethod
    def action(self):
        pass

    def observe(self, sync):
        self.sync = sync