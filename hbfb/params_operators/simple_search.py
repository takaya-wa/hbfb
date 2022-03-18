from hbfb.params_operator import ParamsOperator

class SimpleSearch(ParamsOperator):
    def __init__(self, params, params_info, diff):
        """
        diff => dict
        params_info => {param1:[min, max], param2...}
        """
        super().__init__(params, params_info)
        
        self.first = True
        self.diff = diff 

        self.target_i = 0
        self.target_param = list(self.params.keys())[self.target_i]
        self.plus_minus = 1
        self.add_num = 0
        self.new_param = self.params[self.target_param]
        self.new_params = self.params.copy()

    def action(self):
        if self.sync:
            self._reset()

        success = False
        while not success:
            if self.first:
                self.plus_minus *= -1
                self._first_loop()
            else:
                self._loop()

            if self.params_info[self.target_param][0] >= self.new_param or self.params_info[self.target_param][1] <= self.new_param:
                self.diff[self.target_param] *= 0.8

                if len(self.params) <= self.target_i+1:
                    self.target_i = 0
                else:
                    self.target_i += 1

                self.target_param = list(self.params.keys())[self.target_i]
                print(self.target_param)
                self.first = True
                self._reset()
            else:
                success = True

        self.new_params[self.target_param] = self.new_param
        return self.new_params

    def _first_loop(self):
        if self.plus_minus == -1:
            self.add_num += self.diff[self.target_param]
        
        self.new_param = self.params[self.target_param] + (self.add_num*self.plus_minus)
            
    def _loop(self):
        self.add_num += self.diff[self.target_param]
        self.new_param = self.params[self.target_param] + (self.add_num*self.plus_minus)

    def _reset(self):
        self.add_num = 0

        if self.sync:
            self.params = self.new_params.copy()
            self.first = False
        else:
            self.new_params = self.params.copy()
            
        self.new_param = self.params[self.target_param]