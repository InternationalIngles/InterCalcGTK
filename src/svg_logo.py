import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Rsvg', '2.0')
from gi.repository import Gtk, Rsvg

class SvgLogo(Gtk.DrawingArea):
    def __init__(self, svg_path, size=100):
        super().__init__()
        self.svg_path = svg_path
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self.on_draw)

    def on_draw(self, area, cr, width, height):
        handle = Rsvg.Handle.new_from_file(self.svg_path)
        has_size, intrinsic_width, intrinsic_height = handle.get_intrinsic_size_in_pixels()
        if not has_size:
            intrinsic_width, intrinsic_height = 150, 100

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
