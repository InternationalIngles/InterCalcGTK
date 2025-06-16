import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version('Rsvg', '2.0')
from gi.repository import Adw
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from calculator.calculator_window import Calculator

BASE_DIR = getattr(sys, 'frozen', False) and sys._MEIPASS or os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "icons")

class CalculatorApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.intertech.calculator")

    def do_activate(self, app=None):
        Calculator(self).present()

def main():
    CalculatorApp().run()

if __name__ == "__main__":
    main()
