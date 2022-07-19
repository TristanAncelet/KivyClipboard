from kivy.uix.togglebutton import ToggleButton

class BoardButton(ToggleButton):
    def __init__(self, board_id, board_name, **kwargs):
        super().__init__(**kwargs)
        self.board_id = board_id
        self.text = board_name