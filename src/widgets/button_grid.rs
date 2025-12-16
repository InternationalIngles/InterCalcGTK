use gtk4::prelude::*;
use gtk4::{Grid, Entry};
use crate::widgets::svg_button::SvgButton;
use crate::widgets::svg_logo::SvgLogo;
use crate::utils::safe_eval;

pub struct ButtonGrid {
    pub widget: Grid,
}

impl ButtonGrid {
    pub fn new(entry: &Entry) -> Self {
        let grid = Grid::builder()
            .row_spacing(5)
            .column_spacing(5)
            .row_homogeneous(true)
            .column_homogeneous(true)
            .build();

        let buttons = vec![
            ("7", 0, 0), ("8", 1, 0), ("9", 2, 0), ("/", 3, 0),
            ("4", 0, 1), ("5", 1, 1), ("6", 2, 1), ("*", 3, 1),
            ("1", 0, 2), ("2", 1, 2), ("3", 2, 2), ("-", 3, 2),
            (".", 0, 3), ("0", 1, 3), ("=", 2, 3), ("+", 3, 3),
            ("C", 0, 4), 
        ];

        let icons_dir = "python_original/src/icons"; 

        for (label, col, row) in buttons {
            let icon_name = match label {
                "+" => "plus", "-" => "minus", "*" => "multiply", "/" => "divide",
                "=" => "equal", "." => "dot", "C" => "clear",
                _ => label,
            };
            let svg_path = format!("{}/{}.svg", icons_dir, icon_name);
            
            let svg_btn = SvgButton::new(&svg_path, label);
            let btn_widget = svg_btn.widget; // The gtk::Button

            let entry_clone = entry.clone();
            let label_string = label.to_string();

            btn_widget.connect_clicked(move |_| {
                let current_text = entry_clone.text();
                
                if label_string == "C" {
                    entry_clone.set_text("");
                } else if label_string == "=" {
                    let expr = current_text.as_str();
                    match safe_eval(expr) {
                        Ok(val) => {
                             if val.fract() == 0.0 {
                                 entry_clone.set_text(&format!("{}", val as i64));
                             } else {
                                 entry_clone.set_text(&format!("{}", val));
                             }
                        },
                        Err(_) => entry_clone.set_text("Error"),
                    }
                } else {
                    let mut text = current_text.to_string();
                    if text == "Error" {
                         text = String::new();
                    }
                    text.push_str(&label_string);
                    entry_clone.set_text(&text);
                }
            });

            grid.attach(&btn_widget, col, row, 1, 1);
        }
        
        let logo_path = format!("{}/logo.svg", icons_dir);
        let logo = SvgLogo::new(&logo_path, 100);
        
        logo.widget.set_margin_start(10);
        logo.widget.set_margin_end(10);
        logo.widget.set_margin_top(5);
        logo.widget.set_margin_bottom(5);
        
        grid.attach(&logo.widget, 3, 4, 1, 1);

        Self { widget: grid }
    }
}
