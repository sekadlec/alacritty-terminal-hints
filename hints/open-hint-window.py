#!/usr/bin/env python3
import sys
import os
import gi
import warnings

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class DialogWindow(Gtk.Dialog):
    def __init__(self):
        super().__init__(title="Alacritty Terminal hint")
        self.set_default_size(50, 50)
        self.set_decorated(False)

        box = self.get_content_area()
        box.set_border_width(0)

        if hint_type == "color":
            color_string = hint_text
            color = Gdk.RGBA()
            color.parse(color_string)

            content = Gtk.Label()
            content.set_label(color_string)

            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=DeprecationWarning)
                box.override_background_color(
                    Gtk.StateFlags.NORMAL,
                    color
                )
        
            self.set_position(Gtk.WindowPosition.MOUSE)
        elif hint_type == "image":
            image_path = os.path.expanduser(hint_text)
            content = Gtk.Image.new_from_file(image_path)

            self.set_position(Gtk.WindowPosition.CENTER)
        else:
            content = Gtk.Label()
            content.set_label("Unknown hint type %s with hint text %s" % (hint_type, hint_text))

        box.add(content)

        self.connect('key-press-event', self.on_key_press_event)

        self.add_events(Gdk.EventType.BUTTON_PRESS)
        self.connect('button-press-event', self.on_button_press_event)

    def on_key_press_event(self, widget, event):
        if event.keyval == 65307: # ESC
            Gtk.main_quit()

    def on_button_press_event(self, widget, user_data):
        Gtk.main_quit()

try:
    hint_type = sys.argv[1]
    hint_text = sys.argv[2]
    win = DialogWindow()
    win.connect("close", Gtk.main_quit)
    win.show_all()
    Gtk.main()
except:
    pass
