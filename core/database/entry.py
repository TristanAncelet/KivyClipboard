from core.timer import Timer

class Entry:
    history = None
    timer = Timer
    content = str
    hashed_content = int

    def __init__(self, content) -> None:
        self.timer = Timer.TimeStamp()
        self.content = content
        self.hashed_content = hash(content.lower())
    
    def tick(self):
        self.timer.tick()
    