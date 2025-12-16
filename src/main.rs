use libadwaita::prelude::*;
use libadwaita::Application;

mod window;
mod widgets;
mod utils;
mod about;

fn main() {
    let app = Application::builder()
        .application_id("com.intertech.calculator")
        .build();

    app.connect_activate(build_ui);
    app.run();
}

fn build_ui(app: &Application) {
    let window = window::CalculatorWindow::new(app);
    window.present();
}
