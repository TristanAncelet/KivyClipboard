#!/usr/bin/python3
from ast import arg
import json
from pathlib import Path
import threading
import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.clipboard import Clipboard
from kivy.clock import mainthread
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

import logging
logging.basicConfig(level=None)

global main_view

home_dir = Path.home()
data_dir = home_dir / ".data"
clipboard_file = data_dir / "clipboard.json"

if not data_dir.exists():
    data_dir.mkdir()

if not clipboard_file.exists():
    clipboard_file.touch()


class ClipItem(BoxLayout):
    clip_content = ObjectProperty(None)
    def __init__(self, clip, **kwargs):
        super().__init__(**kwargs)
        self.clip_content.text = clip

class MainView(BoxLayout):
    text_input = ObjectProperty(None)
    clip_area = ObjectProperty(None)
    scroll = ObjectProperty(None)
    clips = list()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load(self):
        if clipboard_file.exists():
            with clipboard_file.open("r") as file:
                for clip in json.load(file):
                    if clip not in self.Clips:
                        self.clip_area.add_widget(ClipItem(clip))
                file.close()

    @mainthread
    def clipboard_trigger(self):
        self.add_to_list()

    
    @property
    def Clips(self):
        clipText = [clip.text for clip in self.UiClips] 
        clipText.reverse()
        return clipText 
    
    @property
    def UiClips(self):
        return self.clip_area.children
    
    @mainthread
    def add_to_list(self):
        if (self.text_input.text != "" or Clipboard.paste() != ""):
            if (self.text_input.text == ""):
                if (Clipboard.paste() != ""):
                    text_to_pass = Clipboard.paste().strip()
            else:
                text_to_pass = self.text_input.text

            self.text_input.text = ""
            if text_to_pass not in self.Clips:
                self.clip_area.add_widget(ClipItem(text_to_pass))


        
    def remove_clip(self, clip:ClipItem):
        self.clip_area.remove_widget(clip)

    def save_clipboard(self):
        with clipboard_file.open('w') as file:
            json.dump(self.Clips, file)
            file.close()

    def move_clip_up(self, clip:ClipItem):
        if clip != self.UiClips[-1]:
            indexOfClip = self.clip_area.children.index(clip)
            indexOfUpperNeighbor = indexOfClip + 1
            self.clip_area.remove_widget(clip)
            self.clip_area.add_widget(clip, indexOfUpperNeighbor)

    def move_clip_down(self, clip:ClipItem):
        if clip != self.UiClips[0]:
            indexOfClip = self.clip_area.children.index(clip)
            indexOfLowerNeighbor = indexOfClip - 1
            self.clip_area.remove_widget(clip)
            self.clip_area.add_widget(clip, indexOfLowerNeighbor)
        

    def clear(self):
        self.clip_area.clear_widgets()



def update_clips(main_view):
    while True:
        main_view.add_to_list()
        time.sleep(2)

class MainApp(App):
    def build(self):
        global main_view
        main_view = MainView()
        clipboard_thread = threading.Thread(target=update_clips,args = (main_view,) , daemon=True)
        clipboard_thread.start()
        self.main_view = main_view
        return self.main_view





if __name__ == "__main__":
    app = MainApp()
    app.run()