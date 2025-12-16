use gtk4::prelude::*;
use gtk4::{Picture};
use gtk4::gio::File;

pub struct SvgLogo {
    pub widget: Picture,
}

impl SvgLogo {
    pub fn new(svg_path: &str, size: i32) -> Self {
        let file = File::for_path(svg_path);
        let picture = Picture::for_file(&file);
        
        picture.set_width_request(size);
        picture.set_height_request(size);
        picture.set_halign(gtk4::Align::Center);
        picture.set_valign(gtk4::Align::Center);

        Self { widget: picture }
    }
}
