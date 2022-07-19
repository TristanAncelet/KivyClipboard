import json
import time
import threading

from kivy.uix.boxlayout import BoxLayout
from kivy.core.clipboard import Clipboard
from kivy.clock import mainthread
from kivy.properties import ObjectProperty

from core.database.history import History
from core.files import clipboard_file

from core.gui.clipitem import ClipItem


class MainView(BoxLayout):
    text_input = ObjectProperty(None)
    clip_area = ObjectProperty(None)
    scroll = ObjectProperty(None)
    history = History
    clips = list()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = History()
        self.clipboard_thread = threading.Thread(target=self.clipboard_thread , daemon=True)
        self.clipboard_thread.start()
        self.load()
        self._trigger_layout()
        self.clip_area._trigger_layout()

    def load(self):
        if clipboard_file.exists():
            with clipboard_file.open("r") as file:
                for clip in json.load(file):
                    self.history.add(clip)
                    if clip not in self.Clips:
                        self.clip_area.add_widget(ClipItem(clip))
                file.close()

    def clipboard_thread(self):

        while True:
            """
            Since any clips that will be added to the history, if something you have in the clipboard
            has the same hash value (aka if they are the same thing) it will not be loaded into the 
            ui
            """
            if not self.history.Contains(Clipboard.paste()):
                self.add_to_list()
            time.sleep(1)

    
    @property
    def Clips(self):
        clipText = [clip.text for clip in self.UiClips] 
        clipText.reverse()
        return clipText 
    
    @property
    def UiClips(self):
        return self.clip_area.children
    
    def have_valid_inputs(self):
        valid_inputs_exist = False

        text_input_is_valid = (self.text_input.text != "")
        clipboard_is_valid = (Clipboard.paste() != "")

        return text_input_is_valid, clipboard_is_valid


        
    
    @mainthread
    def add_to_list(self):

        text_input_is_valid, clipboard_is_valid = self.have_valid_inputs()

        if any([text_input_is_valid, clipboard_is_valid]):
            text_to_pass = ""

            if not text_input_is_valid:
                if clipboard_is_valid:
                    text_to_pass = Clipboard.paste()
            else:
                text_to_pass = self.text_input.text
                self.text_input.text = ""

            if text_to_pass not in self.Clips:
                self.history.add(text_to_pass)
                self.clip_area.add_widget(ClipItem(text_to_pass))


        
    def remove_clip(self, clip:ClipItem):
        self.history.remove_value(clip.clip_content.text)
        self.clip_area.remove_widget(clip)

    def save_clipboard(self):
        with clipboard_file.open('w') as file:
            json.dump(self.Clips, file)
            file.close()

    def move_clip_up(self, clip:ClipItem):
        assert clip in self.UiClips, "The Clip that was provided was not present in the UI"
        if clip != self.UiClips[-1]:
            indexOfClip = self.clip_area.children.index(clip)
            indexOfUpperNeighbor = indexOfClip + 1
            self.clip_area.remove_widget(clip)
            self.clip_area.add_widget(clip, indexOfUpperNeighbor)

    def move_clip_down(self, clip:ClipItem):
        assert clip in self.UiClips, "The Clip that was provided was not present in the UI"
        if clip != self.UiClips[0]:
            indexOfClip = self.clip_area.children.index(clip)
            indexOfLowerNeighbor = indexOfClip - 1
            self.clip_area.remove_widget(clip)
            self.clip_area.add_widget(clip, indexOfLowerNeighbor)
        

    def clear(self):
        self.clip_area.clear_widgets()
 