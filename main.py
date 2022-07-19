#!/usr/bin/python3
from kivy.app import App
   
from core.gui.mainview import MainView


class MainApp(App):
    def build(self):
        return MainView()





if __name__ == "__main__":
    app = MainApp()
    app.run()