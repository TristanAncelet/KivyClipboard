import threading
import time
import re

from charset_normalizer import detect


DEFAULT_TIME = 0, 1, 0

class Time:
    hour = int
    min = int
    sec = int
    thread = threading.Thread

    def __init__(self, hour:int = 0, min:int = 0, sec:int = 0) -> None:
        self.hour = hour
        self.min = min
        self.sec = sec

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

    def __eq__(self, other:'Time'):
        return self.Parts == other.Parts

class Entry:
    history = None
    timer = Time
    content = str
    hashed_content = int

    def __init__(self, history:'History', content) -> None:
        self.timer = Time()
        self.history = history
        self.content = content
        self.hashed_content = hash(content.lower())
    
    def tick(self):
        self.timer.tick()
    


class History(object):
    time_keeping_thread = threading.Thread
    entries = list
    reference = Time

    def __init__(self) -> None:
        self.entries = list()
        _hour, _min, _sec = DEFAULT_TIME
        self.reference = Time(_hour, _min, _sec)
        self.time_keeping_thread = threading.Thread(target=self.increment_entries, daemon=True).start() 

    @property
    def Content(self) -> list[int]:
        return [entry.hashed_content for entry in self.entries]

    def Contains(self, content:str) -> bool:
        doesContain  = False
        item = hash(content.lower())

        for entry in self.Content:
            doesContain = (item == entry)
            if (doesContain):
                break
        return doesContain
    
    def remove_entry(self, entry:Entry):
        self.entries.remove(entry)
    

    def get_entry(self, value:str):
        output = Entry
        _hash = hash(value)
        for entry in self.entries:
            if entry.hashed_content == _hash:
                output = entry
                break
        return output

    def remove_value(self, value:str):
        if self.Contains(value):
            self.entries.remove(self.get_entry(value))

    def add(self, content:str) -> None:
        if not self.Contains(content):
            self.entries.append(Entry(self, content))
            print(f"'{content}' was added to history")

    def start_detection(self):
        self.detect_entries_out_of_time(self.entries)

    def detect_entries_out_of_time(self, itemlist:list):
        if len(itemlist) > 0:
            item = itemlist[0]
            if item.timer == self.reference:
                self.detect_entries_out_of_time(itemlist[1:])
                self.entries.remove(item)
                print(f"'{item.content}' was removed from history")
    
    def increment_entries(self):
        while True:
            for entry in self.entries:
                entry.tick()
            self.start_detection()
            time.sleep(1)