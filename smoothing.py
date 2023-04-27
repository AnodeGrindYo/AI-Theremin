import numpy as np

class DataSmoother:
    
    def __init__(self, smoothing_factor: float = 0.2, change_limit: float = 5) -> None:
        """
        Initialize a DataSmoother object.

        :param smoothing_factor: The factor by which the input data will be smoothed. (default: 0.2)
        :param change_limit: The maximum allowed change in value between consecutive inputs. (default: 5)
        """
        self.smoothing_factor = smoothing_factor
        self.change_limit = change_limit
        self.previous_value = None

    def smooth(self, value: float) -> float:
        """
        Smooth the input value using exponential moving average and limit the change between consecutive values.

        :param value: The input value to be smoothed.
        :return: The smoothed value.
        """
        if self.previous_value is None:
            self.previous_value = value
            return value

        smooth_value = self.previous_value * (1 - self.smoothing_factor) + value * self.smoothing_factor
        limited_value = np.clip(smooth_value, self.previous_value - self.change_limit, self.previous_value + self.change_limit)
        self.previous_value = limited_value

        return limited_value