import numpy as np

class DataSmoother:
    def __init__(self, smoothing_factor=0.2, change_limit=5):
        self.smoothing_factor = smoothing_factor
        self.change_limit = change_limit
        self.previous_value = None

    def smooth(self, value):
        if self.previous_value is None:
            self.previous_value = value
            return value

        smooth_value = self.previous_value * (1 - self.smoothing_factor) + value * self.smoothing_factor
        limited_value = np.clip(smooth_value, self.previous_value - self.change_limit, self.previous_value + self.change_limit)
        self.previous_value = limited_value

        return limited_value