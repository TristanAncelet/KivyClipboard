import threading
import time
from core.timer import Timer
from core.database.entry import Entry

import logging

class History(object):
    """
This class is meant to serve as a container for the history of clips that
the user submits into the clipboard.

It will keep a list of Entry objects that keep track of their time to determine
if it is time for them to be emptied from the main
    """
    time_keeping_thread = threading.Thread
    entries = list
    reference = Timer

    def __init__(self) -> None:
        self.entries = list()
        self.timer = Timer.TimeStamp()
        self.time_keeping_thread = threading.Thread(target=self.increment_entries, daemon=True).start() 

    @property
    def Content(self) -> list[str]:
        # will itterate through the list of entries and return the string associated with each
        return [entry.content for entry in self.entries]
    
    @property
    def Hashes(self) -> list[int]:
        """
        I found that the application had issues with telling if i tried matching using string matching to tell if 
        something was already in history/in the gui.

        However I've had some luck using hashes, as they seem easier to handle when doing == checking.
        """
        return [entry.hashed_content for entry in self.entries]

    def Contains(self, value:str) -> bool:
        """will check if the hash of the value is in the list of hashes, and then return if it was found"""
        item = hash(value.lower())
        return item in self.Hashes
    
    def remove_entry(self, entry:Entry):
        """will remove the entry from the list"""
        self.entries.remove(entry)
    

    def get_entry(self, value:str):
        """
        will take a hash of the passed value and will itterate through the
        entries list while compairing the hash of the value to that of the 
        entry, and will pass it back to the caller.
        """
        output = None
        _hash = hash(value)
        for entry in self.entries:
            if entry.hashed_content == _hash:
                output = entry
                break
        if output == None:
            logging.debug("entry was not found in entrylist despite bieng found by self.Contains()")
        return output

    def remove_value(self, value:str):
        """if the value is contained in entries then it will remove the entry from the list"""
        if self.Contains(value):
            if (result := self.get_entry(value)) != None: #to ensure even if it was not found that it will not crash the program
                self.entries.remove(result)

    def add(self, content:str) -> None:
        """will add a string to the list of Entries if it doesn't already contain it"""
        if not self.Contains(content):
            self.entries.append(Entry(content))

    def start_detection(self):
        self.detect_entries_out_of_time(self.entries)

    def detect_entries_out_of_time(self, entrylist:list):
        """
        using a recursive post-sort search to determine if each entry has met or exceded (not likely) the time limit for them to exist
        in the history.
        """
        if len(entrylist) > 0:
            entry = entrylist[0]
            if abs(entry.timer.Difference(self.timer, True)) == 60: #once I have a config system in place this will be replaced by config.TimeLimit
                if entry != entrylist[-1]:
                    self.detect_entries_out_of_time(entrylist[1:])
                self.entries.remove(entry)

    
    def increment_entries(self):
        #this is intended to be used in a seperate thread to increment each 
        while True:
            self.timer.tick()
            self.start_detection()
            time.sleep(1)
