import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

import os

from svg_button import SvgButton
from svg_logo import SvgLogo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "..", "icons")

class ButtonGrid(Gtk.Grid):
    def __init__(self, calculator_window):
        super().__init__(row_spacing=5, column_spacing=5)
        self.set_row_homogeneous(True)
        self.set_column_homogeneous(True)
        self.calculator = calculator_window

        buttons = [
            ("7", self.on_button_clicked), ("8", self.on_button_clicked), ("9", self.on_button_clicked), ("/", self.on_button_clicked),
            ("4", self.on_button_clicked), ("5", self.on_button_clicked), ("6", self.on_button_clicked), ("*", self.on_button_clicked),
            ("1", self.on_button_clicked), ("2", self.on_button_clicked), ("3", self.on_button_clicked), ("-", self.on_button_clicked),
            (".", self.on_button_clicked), ("0", self.on_button_clicked), ("=", self.on_equal_clicked), ("+", self.on_button_clicked),
            ("C", self.on_clear_clicked),
        ]

        row = 0
        col = 0
        plus_row = plus_col = 0
        for idx, (label, callback) in enumerate(buttons):
            svg_path = self.get_icon_filename(label)
            button = SvgButton(svg_path, label, callback)
            button.set_hexpand(True)
            button.set_vexpand(True)
            button.set_halign(Gtk.Align.FILL)
            button.set_valign(Gtk.Align.FILL)
            self.attach(button, col, row, 1, 1)
            if label == "+":
                plus_row = row
                plus_col = col
            col += 1
            if col > 3:
                col = 0
                row += 1

        logo = SvgLogo(os.path.join(ICONS_DIR, "logo.svg"), size=100)
        logo.set_halign(Gtk.Align.CENTER)
        logo.set_valign(Gtk.Align.CENTER)
        logo.set_margin_start(10)
        logo.set_margin_end(10)
        logo.set_margin_top(5)
        logo.set_margin_bottom(5)
        self.attach(logo, plus_col, plus_row + 1, 1, 1)

    def get_icon_filename(self, label):
        label_map = {
            "+": "plus", "-": "minus", "*": "multiply", "/": "divide",
            "=": "equal", ".": "dot", "C": "clear"
        }
        name = label_map.get(label, label)
        return os.path.join(ICONS_DIR, f"{name}.svg")

    def on_button_clicked(self, button):
        current = self.calculator.entry.get_text()
        label = button.label_value
        self.calculator.entry.set_text(current + label)

    def on_equal_clicked(self, button):
        try:
            result = eval(self.calculator.entry.get_text())
            self.calculator.entry.set_text(str(result))
        except Exception:
            self.calculator.entry.set_text("Error")

    def on_clear_clicked(self, button):
        self.calculator.entry.set_text("")
