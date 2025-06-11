import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
import os

try:
    from ..svg_logo import SvgLogo
except (ImportError, SystemError):
    from svg_logo import SvgLogo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "..", "icons")

class AboutDialog(Adw.Window):
    def __init__(self, parent):
        super().__init__(transient_for=parent, modal=True)
        self.set_default_size(300, 400)
        self.set_title("About")
        self.set_decorated(True)

        vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10,
            margin_top=20,
            margin_bottom=20,
            margin_start=20,
            margin_end=20
        )

        logo = SvgLogo(os.path.join(ICONS_DIR, "logo.svg"), size=300)
        logo.set_halign(Gtk.Align.CENTER)
        logo.set_visible(True)
        vbox.append(logo)

        label = Gtk.Label(label="InterCalculator\nVersion 1.0\nBy Nilton Perim")
        label.set_justify(Gtk.Justification.CENTER)
        vbox.append(label)

        button = Gtk.Button(label="Close")
        button.connect("clicked", lambda btn: self.close())
        vbox.append(button)

        self.set_content(vbox)
