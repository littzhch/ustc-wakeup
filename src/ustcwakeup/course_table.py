from functools import total_ordering


@total_ordering
class Time:
    """
    一天中的一个时间点，使用 24 小时制
    """
    def __init__(self, hour: int, minute: int):
        assert hour >= 0 and hour <= 23 and minute >= 0 and minute <= 59
        self.__hour = hour
        self.__minute = minute
        self.__minutes = hour * 60 + minute
        
    def hour(self) -> int:
        """
        获取小时数(0~23)
        """
        return self.__hour
    
    def minute(self) -> int:
        """
        获取分钟数
        """
        return self.__minute

    def __int__(self):
        return self.__minutes

    def __eq__(self, other):
        return int(self) == int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __sub__(self, other) -> int:
        return int(self) - int(other)

    def __add__(self, other: int) -> "Time":
        minutes = int(self) + other
        hour = minutes // 60
        minute = minutes % 60
        return Time(hour, minute)
    

@total_ordering
class TimePeriod:
    def __init__(self, start_time: Time, end_time: Time):
        self.start_time = start_time
        self.end_time = end_time

    def __eq__(self, other):
        return self.start_time == other.start_time \
               and self.end_time == other.end_time

    def __gt__(self, other):
        return self.start_time > other.start_time

    def __len__(self):
        return self.end_time - self.start_time

    def __sub__(self, other):
        return self.start_time - other.end_time

    def get_info(self):
        return {
            "endTime": str(self.end_time),
            "node": None,
            "startTime": str(self.start_time),
            "timeTable": None
        }