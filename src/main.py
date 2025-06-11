import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version('Rsvg', '2.0')
from gi.repository import Gtk, Gio, Rsvg, Pango, Gdk, Adw

import sys
import os

try:
    # Try relative imports (for 'python -m src.main')
    from .svg_button import SvgButton
    from .svg_logo import SvgLogo
    from .calculator import Calculator
except (ImportError, SystemError):
    # Fallback to absolute imports (for 'python src/main.py')
    from svg_button import SvgButton
    from svg_logo import SvgLogo
    from calculator import Calculator

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ICONS_DIR = os.path.join(BASE_DIR, "icons")

class CalculatorApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.intertech.calculator")

    def do_activate(self, app=None):
        win = Calculator(self)
        win.present()

def main():
    app = CalculatorApp()
    app.run()

if __name__ == "__main__":
    main()
