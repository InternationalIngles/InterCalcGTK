import gi
gi.require_version("Gtk", "4.0")
gi.require_version('Rsvg', '2.0')
from gi.repository import Gtk, Gio, Rsvg, Pango

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "icons")

# Button
class SvgButton(Gtk.Button):
    def __init__(self, svg_path, label_value, callback):
        super().__init__()
        self.svg_path = svg_path
        self.label_value = label_value

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_content_width(70)
        self.drawing_area.set_content_height(70)
        self.drawing_area.set_draw_func(self.on_draw)

        self.set_child(self.drawing_area)
        self.connect("clicked", callback)

    def on_draw(self, area, cr, width, height):
        handle = Rsvg.Handle.new_from_file(self.svg_path)
        dimensions = handle.get_dimensions()

        scale_x = width / dimensions.width
        scale_y = height / dimensions.height
        scale = min(scale_x, scale_y)

        new_width = dimensions.width * scale
        new_height = dimensions.height * scale

        offset_x = (width - new_width) / 2
        offset_y = (height - new_height) / 2

        cr.translate(offset_x, offset_y)
        cr.scale(scale, scale)

        handle.render_cairo(cr)

# SVG Logo at the bottom
class SvgLogo(Gtk.DrawingArea):
    def __init__(self, svg_path, size=100):
        super().__init__()
        self.svg_path = svg_path
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self.on_draw)

    def on_draw(self, area, cr, width, height):
        handle = Rsvg.Handle.new_from_file(self.svg_path)
        dimensions = handle.get_dimensions()

        scale_x = width / dimensions.width
        scale_y = height / dimensions.height
        scale = min(scale_x, scale_y)

        new_width = dimensions.width * scale
        new_height = dimensions.height * scale

        offset_x = (width - new_width) / 2
        offset_y = (height - new_height) / 2

        cr.translate(offset_x, offset_y)
        cr.scale(scale, scale)

        handle.render_cairo(cr)

# Calculator Window
class Calculator(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("InterCalc")
        self.set_default_size(250, 300)

        self.dark_mode = False

        # HeaderBar
        header = Gtk.HeaderBar()
        header.set_title_widget(Gtk.Label(label="InterCalc"))
        self.set_titlebar(header)
        #Hamburguer Menu
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

        header.pack_end(menu_button)

        # Outer box with margin for aspect ratio
        outer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        outer_box.set_margin_start(20)
        outer_box.set_margin_end(20)
        outer_box.set_margin_top(20)
        outer_box.set_margin_bottom(20)
        self.set_child(outer_box)

        # Aspect preserving frame
        frame = Gtk.AspectFrame(ratio=0.7, obey_child=False)
        outer_box.append(frame)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        frame.set_child(main_box)

        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.entry.set_vexpand(False)
        self.entry.set_margin_bottom(10)
        self.entry.set_size_request(-1, 60)

        # Result screen
        context = self.entry.get_style_context()
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b'''
            entry {
                font-family: "Inter";
                font-size: 60px;
            }
        ''')
        context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

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
            # Track the position of the plus button
            if label == "+":
                plus_row = row
                plus_col = col
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Logo
        logo = SvgLogo(os.path.join(ICONS_DIR, "logo.svg"), size=80)
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
        about = Gtk.HeaderBar()
        about.set_title_widget(Gtk.Label(label="About"))
        about = Gtk.Dialog(title="About", transient_for=self, modal=True)
        about.set_default_size(200, 300)

        
        content = about.get_content_area()

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin_top=20, margin_bottom=20, margin_start=20, margin_end=20)
        content.append(vbox)
        logo = SvgLogo(os.path.join(ICONS_DIR, "logo.svg"), size=200)  
        logo.set_halign(Gtk.Align.CENTER)
        vbox.append(logo)

        label = Gtk.Label(label="InterCalculator\nVersion 0.3\nBy Nilton Perim")
        label.set_justify(Gtk.Justification.CENTER)
        vbox.append(label)

        button = Gtk.Button(label="Close")
        button.connect("clicked", lambda btn: about.close())
        vbox.append(button)

        about.show()

    def on_toggle_mode(self, button):
        settings = Gtk.Settings.get_default()
        self.dark_mode = not self.dark_mode
        settings.set_property("gtk-application-prefer-dark-theme", self.dark_mode)

# Application
class CalculatorApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.intertech.calculator")

    def do_activate(self, app=None):
        win = Calculator(self)
        win.present()

def main():
    app = CalculatorApp()
    app.run()

if __name__ == "__main__":
    main()
