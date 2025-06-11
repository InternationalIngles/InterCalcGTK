import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Rsvg', '2.0')
from gi.repository import Gtk, Rsvg

class SvgButton(Gtk.Button):
    def __init__(self, svg_path, label_value, callback):
        super().__init__()
        self.svg_path = svg_path
        self.label_value = label_value

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_content_width(80)
        self.drawing_area.set_content_height(80)
        self.drawing_area.set_draw_func(self.on_draw)

        self.set_child(self.drawing_area)
        self.connect("clicked", callback)

    def on_draw(self, area, cr, width, height):
        handle = Rsvg.Handle.new_from_file(self.svg_path)
        has_size, intrinsic_width, intrinsic_height = handle.get_intrinsic_size_in_pixels()
        if not has_size:
            intrinsic_width, intrinsic_height = 80, 80

        scale_x = width / intrinsic_width
        scale_y = height / intrinsic_height
        scale = min(scale_x, scale_y)

        new_width = intrinsic_width * scale
        new_height = intrinsic_height * scale

        offset_x = (width - new_width) / 2
        offset_y = (height - new_height) / 2

        cr.translate(offset_x, offset_y)
        cr.scale(scale, scale)

        rect = Rsvg.Rectangle()
        rect.x = 0
        rect.y = 0
        rect.width = intrinsic_width
        rect.height = intrinsic_height
        handle.render_document(cr, rect)
