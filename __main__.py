#!/usr/bin/python3
import json
from kivy import *
import os
from kivy.app import App
import pyclip
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class ClipItem(BoxLayout):
    clip_content = ObjectProperty(None)

    def __init__(self,clip_text:str ,**kwargs):
        super().__init__(**kwargs)
        self.clip_content.text = clip_text

class MainView(BoxLayout):
    text_input = ObjectProperty(None)
    clip_area = ObjectProperty(None)
    scroll = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load(self):
        self.clip_area.clear_widgets()
        if "clipboard.json" in os.listdir("files"):
            with open("files/clipboard.json", 'r') as file:
                for clip in json.load(file):
                    newClip = ClipItem(clip)
                    self.clip_area.add_widget(newClip) 

    def add_to_list(self):
        if (self.text_input.text != "" or pyclip.paste() != ""):
            if (self.text_input.text == ""):
                if (pyclip.paste() != ""):
                    text_to_pass = pyclip.paste().decode()
            else:
                text_to_pass = self.text_input.text
                self.text_input.text = ""

            newClip =  ClipItem(text_to_pass)
            self.clip_area.add_widget(newClip)

        
    def remove_clip(self, clip):
        self.clip_area.remove_widget(clip)

    def save_clipboard(self):
        clips = list()

        for item in self.clip_area.children:
            clips.append(item.text)

        with open("files/clipboard.json", 'w') as file:
            json.dump(clips, file)
            file.close()
            



class MainApp(App):
    def build(self):
        self.main_view = MainView()
        return self.main_view
        self.main_view.clip_area.do_layout()
if __name__ == "__main__":
    MainApp().run()
