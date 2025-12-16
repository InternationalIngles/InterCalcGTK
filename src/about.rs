use libadwaita::prelude::*;
use gtk4::{Button, Box, Label, Orientation, Justification};
use crate::widgets::svg_logo::SvgLogo;

pub struct AboutDialog;

impl AboutDialog {
    pub fn present(parent: &impl IsA<gtk4::Window>) {
        let window = libadwaita::Window::builder()
            .transient_for(parent)
            .modal(true)
            .default_width(300)
            .default_height(400)
            .title("About")
            .build();

        let vbox = Box::builder()
            .orientation(Orientation::Vertical)
            .spacing(10)
            .margin_top(20)
            .margin_bottom(20)
            .margin_start(20)
            .margin_end(20)
            .build();

        let icons_dir = "python_original/src/icons";
        let logo_path = format!("{}/logo.svg", icons_dir);
        let logo = SvgLogo::new(&logo_path, 300);
        logo.widget.set_visible(true);
        vbox.append(&logo.widget);

        let label = Label::builder()
            .label("InterCalculator\nVersion 1.0\nBy Nilton Perim")
            .justify(Justification::Center)
            .build();
        vbox.append(&label);

        let close_btn = Button::with_label("Close");
        let win_clone = window.clone();
        close_btn.connect_clicked(move |_| {
            win_clone.close();
        });
        vbox.append(&close_btn);

        window.set_content(Some(&vbox));
        window.present();
    }
}
