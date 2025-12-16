use gtk4::prelude::*;
use gtk4::{Button, Picture};
use gtk4::gio::File;

pub struct SvgButton {
    pub widget: Button,
}

impl SvgButton {
    pub fn new(svg_path: &str, label_value: &str) -> Self {
        let file = File::for_path(svg_path);
        let picture = Picture::for_file(&file);
        
        picture.set_width_request(60);
        picture.set_height_request(60);

        let button = Button::builder()
            .child(&picture)
            .hexpand(true)
            .vexpand(true)
            .tooltip_text(label_value)
            .build();

        Self {
            widget: button,
        }
    }
}
