
DEFAULT_TIME = 0, 1, 0
class Timer:
    hour = int
    min = int
    sec = int

    def __init__(self, _hour:int = None, _min:int = None, _sec:int = None) -> None:

        if not all([_hour, _min, _sec]):
            _hour, _min, _sec = DEFAULT_TIME

        self.hour = _hour
        self.min = _min
        self.sec = _sec
    
    @classmethod
    def TimeStamp(cls):
        from datetime import datetime
        _hour, _min, _sec = (int(item) for item in datetime.today().strftime("%H:%M:%S").split(":"))
        return cls(_hour, _min, _sec)

    def tick(self):
        self.sec += 1
        if self.sec == 60:
            self.sec = 0
            self.min += 1
            if self.min == 60:
                self.min = 0
                self.hour += 1
    @property
    def Parts(self):
        return [self.hour, self.min, self.sec]

    @property
    def HasValue(self):
        return any([part != 0 for part in self.Parts])

    def __str__(self):
        return ":".join([self.Parts])

    def __eq__(self, other:'Timer'):
        return self.Parts == other.Parts

    @property
    def InSeconds(self):
        return (3600 * self.hour) + (60 * self.min) + self.sec

    def __gt__(self, other:'Timer') -> bool:
        return self.InSeconds > other.InSeconds
        
    def __lt__(self, other:'Timer') -> bool:
        return not self.__gt__(other)
    
    def Compare(self, other:'Timer'):
        output = int

        selfTime = self.InSeconds
        otherTime = other.InSeconds

        if selfTime < otherTime: #is less than
            output = -1
        elif selfTime == otherTime: #is equal to
            output = 0
        elif selfTime > otherTime: #is greater than
            output = 1
        
        return output

    
    def Difference(self, other:'Timer', using_seconds:bool = False):
        output = None
        if using_seconds:
            output = self.InSeconds - other.InSeconds
        else:
            output = ((item1 - item2) for item1, item2 in zip(other.Parts, self.Parts))

        return output

