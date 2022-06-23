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

    
    @property
    def Clips(self):
        clipText = [clip.text for clip in self.UiClips] 
        clipText.reverse()
        return clipText 
    
    @property
    def UiClips(self):
        return self.clip_area.children
    

    def add_to_list(self):
        if (self.text_input.text != "" or pyclip.paste() != ""):
            if (self.text_input.text == ""):
                if (pyclip.paste() != ""):
                    text_to_pass = pyclip.paste().decode()
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



class MainApp(App):
    def build(self):
        self.main_view = MainView()
        return self.main_view

if __name__ == "__main__":
    app = MainApp()
    app.run()
    