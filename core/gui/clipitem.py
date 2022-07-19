from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

class ClipItem(BoxLayout):
    clip_content = ObjectProperty(None)
    def __init__(self, clip, **kwargs):
        super().__init__(**kwargs)
        self.clip_content.text = clip