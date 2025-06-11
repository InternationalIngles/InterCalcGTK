import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Gdk, Adw
import os

try:
    from .svg_button import SvgButton
    from .svg_logo import SvgLogo
except (ImportError, SystemError):
    from svg_button import SvgButton
    from svg_logo import SvgLogo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "icons")

class Calculator(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("InterCalc")
        self.set_default_size(250, 300)

        self.dark_mode = False

        # Main vertical box
        outer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0) 
        self.set_content(outer_box)

        # HeaderBar as first child of the box
        header = Adw.HeaderBar()
        header.set_title_widget(Gtk.Label(label="InterCalc"))

        # Hamburguer Menu
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

        # Content box with margins
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content_box.set_margin_start(20)
        content_box.set_margin_end(20)
        content_box.set_margin_top(20)
        content_box.set_margin_bottom(20)
        outer_box.append(content_box)

        # Done it to preserve aspect ratio
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

        # Button Grid
        grid = Gtk.Grid(row_spacing=5, column_spacing=5)
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        main_box.append(grid)

        buttons = [
            ("7", self.on_button_clicked), ("8", self.on_button_clicked), ("9", self.on_button_clicked), ("/", self.on_button_clicked),
            ("4", self.on_button_clicked), ("5", self.on_button_clicked), ("6", self.on_button_clicked), ("*", self.on_button_clicked),
            ("1", self.on_button_clicked), ("2", self.on_button_clicked), ("3", self.on_button_clicked), ("-", self.on_button_clicked),
            (".", self.on_button_clicked), ("0", self.on_button_clicked), ("=", self.on_equal_clicked), ("+", self.on_button_clicked),
            ("C", self.on_clear_clicked),
        ]

        row = 0
        col = 0
        for idx, (label, callback) in enumerate(buttons):
            svg_path = self.get_icon_filename(label)
            button = SvgButton(svg_path, label, callback)
            button.set_hexpand(True)
            button.set_vexpand(True)
            button.set_halign(Gtk.Align.FILL)
            button.set_valign(Gtk.Align.FILL)
            grid.attach(button, col, row, 1, 1)
            if label == "+":
                plus_row = row
                plus_col = col
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Logo
        logo = SvgLogo(os.path.join(ICONS_DIR, "logo.svg"), size=100)
        logo.set_halign(Gtk.Align.CENTER)
        logo.set_valign(Gtk.Align.CENTER)
        logo.set_margin_start(10)
        logo.set_margin_end(10)
        logo.set_margin_top(5)
        logo.set_margin_bottom(5)
        grid.attach(logo, plus_col, plus_row + 1, 1, 1)

    def get_icon_filename(self, label):
        label_map = {
            "+": "plus", "-": "minus", "*": "multiply", "/": "divide",
            "=": "equal", ".": "dot", "C": "clear"
        }
        name = label_map.get(label, label)
        return os.path.join(ICONS_DIR, f"{name}.svg")

    def on_button_clicked(self, button):
        current = self.entry.get_text()
        label = button.label_value
        self.entry.set_text(current + label)

    def on_equal_clicked(self, button):
        try:
            result = eval(self.entry.get_text())
            self.entry.set_text(str(result))
        except Exception:
            self.entry.set_text("Error")

    def on_clear_clicked(self, button):
        self.entry.set_text("")
    #About
    def on_about_clicked(self, button):
        about = Adw.Window(transient_for=self, modal=True)
        about.set_default_size(300, 400)
        about.set_title("About")
        about.set_decorated(True)

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
        button.connect("clicked", lambda btn: about.close())
        vbox.append(button)

        about.set_content(vbox)
        about.present()

    def on_toggle_mode(self, button):
        style_manager = Adw.StyleManager.get_default()
        self.dark_mode = not self.dark_mode
        style_manager.set_color_scheme(
            Adw.ColorScheme.FORCE_DARK if self.dark_mode else Adw.ColorScheme.FORCE_LIGHT
        )