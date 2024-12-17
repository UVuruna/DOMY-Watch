'''
Circle Example
==============

This example exercises circle (ellipse) drawing. You should see sliders at the
top of the screen with the Kivy logo below it. The sliders control the
angle start and stop and the height and width scales. There is a button
to reset the sliders. The logo used for the circle's background image is
from the kivy/data directory. The entire example is coded in the
kv language description.
'''

from kivy.app import App
from kivy.lang import Builder
import os

current_folder = os.path.dirname(os.path.abspath(__file__))
file_name = "Circle.kv"
file_path = os.path.join(current_folder, file_name)

class CircleApp(App):
    def build(self):
        
        return Builder.load_file(file_path)


CircleApp().run()