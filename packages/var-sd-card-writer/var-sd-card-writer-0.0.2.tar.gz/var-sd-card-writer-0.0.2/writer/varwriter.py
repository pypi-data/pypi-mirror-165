#!/usr/bin/env python3

# Copyright 2022 Variscite LTD
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import gi
gi.require_versions({'Gdk': "3.0", 'Gtk': "3.0"})
from gi.repository import Gdk, Gtk
import os

from writer.config import CACHEDIR
from writer.menubar import MenuBar
from writer.select import SelectImage
from writer.welcome import MainWindow


settings = Gtk.Settings.get_default()
settings.set_property("gtk-theme-name", "Yaru")
settings.set_property("gtk-application-prefer-dark-theme", False)  # if you want use dark theme, set second arg to True


class VarWriterGUI(Gtk.Window):
    def __init__(self):
        super(VarWriterGUI, self).__init__(title="Var Writer")
        self.set_default_size(960, 590)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)

        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path(os.path.join(CACHEDIR, "assets", "writer.css"))

        self.ftp_image = None
        self.local_image = None
        self.device = None
        self.devices = []

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(main_box)

        menu_bar = MenuBar(self)
        main_box.pack_start(menu_bar, False, False, 0)

        self.main_container = Gtk.Box()
        self.main_container.set_name("MainBox")
        main_box.pack_start(self.main_container, True, True, 0)
        self.show_all()

        self.main_window = MainWindow(self)
        self.ftp_image_window = SelectImage(self)
        self.flash_image_window = Gtk.Box()

        self.main_container.add(self.main_window)
        self.main_container.add(self.ftp_image_window)
        self.main_container.add(self.flash_image_window)
        self.main_container.show()


def main():
    os.makedirs(CACHEDIR, exist_ok=True)
    app = VarWriterGUI()
    app.set_icon_from_file(os.path.join(CACHEDIR, "assets", "variscite_icon.png"))
    app.connect('delete-event', Gtk.main_quit)
    app.main_window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
