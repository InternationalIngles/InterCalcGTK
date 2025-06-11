import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Gdk, Adw
import os

from .button_grid import ButtonGrid
from .about_dialog import AboutDialog

try:
    from ..svg_logo import SvgLogo
except (ImportError, SystemError):
    from svg_logo import SvgLogo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "..", "icons")

class Calculator(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("InterCalc")
        self.set_default_size(250, 300)
        self.dark_mode = False

        outer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_content(outer_box)

        header = Adw.HeaderBar()
        header.set_title_widget(Gtk.Label(label="InterCalc"))

        menu_button = Gtk.MenuButton()
        icon = Gtk.Image.new_from_icon_name("open-menu-symbolic")
        menu_button.set_child(icon)

        menu = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin_top=10, margin_bottom=10, margin_start=10, margin_end=10)

        about_btn = Gtk.Button(label="About")
        about_btn.connect("clicked", self.on_about_clicked)
        menu.append(about_btn)

        mode_btn = Gtk.Button(label="Toggle Light/Dark Mode")
        mode_btn.connect("clicked", self.on_toggle_mode)
        menu.append(mode_btn)

        popover = Gtk.Popover()
        popover.set_child(menu)
        menu_button.set_popover(popover)

        header.pack_start(menu_button)
        outer_box.append(header)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content_box.set_margin_start(20)
        content_box.set_margin_end(20)
        content_box.set_margin_top(20)
        content_box.set_margin_bottom(20)
        outer_box.append(content_box)

        frame = Gtk.AspectFrame(ratio=0.7, obey_child=False)
        content_box.append(frame)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        frame.set_child(main_box)

        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.entry.set_vexpand(False)
        self.entry.set_margin_bottom(10)
        self.entry.set_size_request(-1, 60)
        self.entry.add_css_class("calc-entry")

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b'''
            .calc-entry {
                font-family: "Exo 2";
                font-size: 90px;
            }
        ''')
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        main_box.append(self.entry)

        # Use ButtonGrid class
        button_grid = ButtonGrid(self)
        main_box.append(button_grid)

    def on_about_clicked(self, button):
        AboutDialog(self).present()

    def on_toggle_mode(self, button):
        style_manager = Adw.StyleManager.get_default()
        self.dark_mode = not self.dark_mode
        style_manager.set_color_scheme(
            Adw.ColorScheme.FORCE_DARK if self.dark_mode else Adw.ColorScheme.FORCE_LIGHT
        )
