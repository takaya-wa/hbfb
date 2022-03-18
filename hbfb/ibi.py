class Ibi:
    def __init__(self, threshold=550):
        self._reset(threshold)
        self.get_sample = False

    def set_sample_list(self): # 動作確認用
        self.detection_time_list = []
        self.threshold_list = []
        self.get_sample = True

    def _reset(self, threshold):
        self.threshold = threshold
        self.defalt_threshold = threshold
        self.p = self.threshold
        self.t = self.threshold
        self.detection = False
        self.detection_time = 0
        self.first_detection = True
        self.ibi = 0
        self.under_threshold = False

    def calc_ibi(self, signal):
        """
        signal => [(signal, time), ...]
        """
        error_log = {"No signal":False, "Error":False}
        ibi_list = []

        for signal, time in signal:
            if self.get_sample: 
                self.threshold_list.append(self.threshold)
            
            n = time - self.detection_time

            if signal == 0:
                error_log["No signal"] = True
                continue

            # check peak and trough
            if self.p < signal and self.threshold < signal:
                self.p = signal
            
            if self.t > signal and self.threshold > signal and n > self.ibi*3/5:
                self.t = signal

            # check a beat
            if signal > self.threshold and n > 250 and n > self.ibi*3/5 and not self.detection and self.under_threshold:
                if self.first_detection:
                    self.first_detection = False
                else:
                    self.ibi = n
                    if not self.first_detection: # IBIの計算を安定させるために最初の検知は追加しない
                        ibi_list.append(self.ibi)
                
                self.detection_time = time
                if self.get_sample:
                    self.detection_time_list.append(self.detection_time)

                self.detection = True
                self.under_threshold = False

            # set threshold
            if signal < self.threshold and self.detection:
                self.detection = False           
                self.threshold = (self.p - self.t) / 2 + self.t
                self.p = self.threshold
                self.t = self.threshold
            
            # 以下、異常対策
            # 閾値変更後のシグナルチェック
            if not self.detection and  signal < self.threshold:
                self.under_threshold = True

            # reset
            if n > 1500 or (signal > self.threshold and (n < 250 or n < self.ibi*3/5) and not self.detection and self.under_threshold):  
                self._reset(self.defalt_threshold)
                self.detection_time = time
                error_log["Error"] = True
        
        return ibi_list, error_log