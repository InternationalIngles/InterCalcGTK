use libadwaita::prelude::*;
use gtk4::{Box, Orientation, Label, MenuButton, Button, Popover, AspectFrame, Entry, CssProvider, gdk};
use libadwaita::{ApplicationWindow, HeaderBar, StyleManager, ColorScheme};
use crate::widgets::button_grid::ButtonGrid;
use crate::about::AboutDialog;

pub struct CalculatorWindow {
    pub widget: ApplicationWindow,
}

impl CalculatorWindow {
    pub fn new(app: &libadwaita::Application) -> Self {
        let window = ApplicationWindow::builder()
            .application(app)
            .title("InterCalculator")
            .default_width(250)
            .default_height(300)
            .resizable(true)
            .build();

        let outer_box = Box::new(Orientation::Vertical, 0);
        window.set_content(Some(&outer_box));

        let header = HeaderBar::new();
        let title = Label::new(Some("InterCalc"));
        header.set_title_widget(Some(&title));

        let menu_btn = MenuButton::new();
        menu_btn.set_icon_name("open-menu-symbolic");

        let menu_box = Box::builder()
            .orientation(Orientation::Vertical)
            .spacing(6)
            .margin_top(10)
            .margin_bottom(10)
            .margin_start(10)
            .margin_end(10)
            .build();

        let about_btn = Button::with_label("About");
        let win_weak = window.downgrade();
        about_btn.connect_clicked(move |_| {
            if let Some(win) = win_weak.upgrade() {
                AboutDialog::present(&win);
            }
        });
        menu_box.append(&about_btn);

        let mode_btn = Button::with_label("Toggle Light/Dark Mode");
        mode_btn.connect_clicked(|_| {
            let manager = StyleManager::default();
            if manager.is_dark() {
                manager.set_color_scheme(ColorScheme::ForceLight);
            } else {
                manager.set_color_scheme(ColorScheme::ForceDark);
            }
        });
        menu_box.append(&mode_btn);

        let popover = Popover::new();
        popover.set_child(Some(&menu_box));
        menu_btn.set_popover(Some(&popover));

        header.pack_start(&menu_btn);
        outer_box.append(&header);

        let content_box = Box::builder()
            .orientation(Orientation::Vertical)
            .spacing(10)
            .margin_top(20)
            .margin_bottom(20)
            .margin_start(20)
            .margin_end(20)
            .build();
        outer_box.append(&content_box);

        let frame = AspectFrame::builder()
            .ratio(0.7)
            .obey_child(false)
            .build();
        content_box.append(&frame);

        let main_box = Box::new(Orientation::Vertical, 10);
        frame.set_child(Some(&main_box));

        let entry = Entry::new();
        entry.set_hexpand(true);
        entry.set_vexpand(false);
        entry.set_margin_bottom(10);
        entry.set_size_request(-1, 60);
        entry.add_css_class("calc-entry");
        
        let provider = CssProvider::new();
        provider.load_from_data("
            .calc-entry {
                font-family: \"Exo 2\";
                font-size: 45px;
            }
        ");
        gtk4::style_context_add_provider_for_display(
            &gdk::Display::default().expect("No display"),
            &provider,
            gtk4::STYLE_PROVIDER_PRIORITY_USER,
        );

        main_box.append(&entry);

        let button_grid = ButtonGrid::new(&entry);
        main_box.append(&button_grid.widget);

        Self { widget: window }
    }

    pub fn present(&self) {
        self.widget.present();
    }
}
