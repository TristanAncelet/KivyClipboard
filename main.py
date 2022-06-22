#!/usr/bin/python3
import json
import pyclip
from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty


home_dir = Path.home()
data_dir = home_dir / ".data"
clipboard_file = data_dir / "clipboard.json"

if not data_dir.exists():
    data_dir.mkdir()

if not clipboard_file.exists():
    clipboard_file.touch()


class ClipItem(BoxLayout):
    clip_content = ObjectProperty(None)
    text = StringProperty("unset")




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
                    if clip not in self.ClipboardClips:
                        self.clips.append(ClipItem(clip))
        self.set_clips()

    
    @property
    def Clips(self):
        return self.clips

    @property
    def ClipboardClips(self):
        return [clip.text for clip in self.clips]
    
    @property
    def UiClips(self):
        return self.clip_area.children
    
                
    def set_clips(self):
        for clip in self.UiClips:
            if clip not in self.clips:
                self.clip_area.remove_widget(clip)

        for clip in self.clips:
            if clip not in self.UiClips:
                self.clip_area.add_widget(clip)



    def add_to_list(self):
        if (self.text_input.text != "" or pyclip.paste() != ""):
            if (self.text_input.text == ""):
                if (pyclip.paste() != ""):
                    text_to_pass = pyclip.paste().decode()
            else:
                text_to_pass = self.text_input.text

            self.text_input.text = ""
            if text_to_pass not in self.ClipboardClips:
                clip = ClipItem()
                self.clips.append(ClipItem())
                self.set_clips()


        
    def remove_clip(self, clip:ClipItem):
        self.clips.remove(clip)
        self.set_clips()

    def save_clipboard(self):
        with clipboard_file.open('w') as file:
            json.dump(self.ClipboardClips, file)
            file.close()

    def rclear(self, items:list):
        if  len(items) > 0:
            item = items[0]
            items.remove(item)
            self.rclear(items)

            
    def clear(self):
        for clip in self.clips:
            self.remove_clip(clip)



class MainApp(App):
    def build(self):
        self.main_view = MainView()
        return self.main_view

if __name__ == "__main__":
    app = MainApp()
    app.run()
    