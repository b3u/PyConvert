"""
PyConvert
(c) 2020 Binyamin Green
"""

import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GdkPixbuf, GLib
class Gui(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        GLib.set_application_name('PyConvert')

        icon_size = Gtk.IconSize.lookup(Gtk.IconSize.SMALL_TOOLBAR)
        self.icon = GdkPixbuf.Pixbuf.new_from_file_at_size("logo.svg", icon_size[1], icon_size[2])

        self.set_default_icon(self.icon)
        self.set_title("PyConvert")
        self.set_border_width(10)

        self.convert_usd = {
            "CAD": {"name": "Canadian Dollar", "rate": 1.33, "prefix": "$"},
            "EUR": {"name": "Euro", "rate": 0.92, "prefix": "€"},
            "GBP": {"name": "British Pound", "rate": 0.77, "prefix": "£"},
            "ILS": {"name": "Israeli New Shekel", "rate": 3.42, "prefix": "₪"},
            "JPY": {"name": "Japanese Yen", "rate": 109.74, "prefix": "¥"},
        }

        self.header_bar()
        # self.set_interactive_debugging(True)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(6)
        self.grid.set_column_spacing(6)
        
        self.entry = Gtk.SpinButton.new_with_range(0, 9999, 0.10)
        self.entry.set_digits(2)

        self.grid.attach(self.entry, 0, 0, 1, 1)

        self.grid.attach(Gtk.Label(label="USD as "), 1, 0, 1, 1)
        
        self.dropdown = Gtk.ComboBoxText()
        
        for key in self.convert_usd:
            self.dropdown.append(key, self.convert_usd[key]["name"])

        self.grid.attach(self.dropdown, 2, 0, 2, 1)

        
        btn_convert = Gtk.Button.new_with_label(label="Convert")
        btn_convert.connect("clicked", self.convert)

        self.grid.attach(btn_convert, 0, 1, 2, 1)

        self.output = Gtk.Entry(placeholder_text="0.00", editable=False)
        self.grid.attach(self.output, 2, 1, 1, 1)

        self.add(self.grid)

    def convert(self, *args):
        current_input = float(self.entry.get_value())
        
        # Handle Errors
        if not current_input:
            return self.show_popover(self.entry, "Input should be greater than zero")
        elif not self.dropdown.props.active_id:
            return self.show_popover(self.dropdown, "Choose a currency")

        # Calculate
        current_dict = self.convert_usd[self.dropdown.props.active_id] 
        amount = round(current_input * current_dict.get("rate"), 2)
        self.output.set_text(current_dict.get("prefix") + ' ' + format(amount, '.2f'))

    def header_bar(self):
        widget = Gtk.HeaderBar()
        widget.set_show_close_button(True)
        widget.set_title(self.props.title);
        
        # Theme should govern whether app icon shows
        # widget.pack_start(Gtk.Image.new_from_pixbuf(self.icon))
        
        about_icon = Gtk.Button.new_from_icon_name("help-about", 2)
        about_icon.connect("clicked", self.about_dialog)
        about_icon.set_tooltip_text("About this Program")
        widget.pack_end(about_icon)

        self.set_titlebar(widget)
    def show_popover(self, parent, text):
        popover = Gtk.Popover.new(relative_to=parent)
        popover.set_border_width(4)
        popover.add(Gtk.Label(label=text, visible=True))
        popover.popup()
        popover.connect("closed", lambda widget: widget.destroy())

    def about_dialog(self, *args):
        widget = Gtk.AboutDialog()
        widget.set_license_type(Gtk.License.MIT_X11)
        widget.set_authors(["Binyamin Green https://binyam.in"])
        widget.set_version("1.0.0")
        widget.set_website("https://gitlab.com/b3u/pyconvert/")
        widget.set_website_label("Source Code")
        widget.set_logo(GdkPixbuf.Pixbuf.new_from_file_at_size('logo.svg', 48, 48))
        widget.connect("response", lambda w, b: w.close())
        widget.run()

if __name__ == "__main__":
    app = Gui()
    app.show_all()
    app.connect("destroy", Gtk.main_quit)
    Gtk.main()
