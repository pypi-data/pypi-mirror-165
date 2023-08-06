# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from re import L
import gi
gi.require_version('Gtk', "3.0")
from gi.repository import GLib, Gtk
import os
from threading import Thread

from writer.config import VAR_MODULES
from writer.utils import get_images_list_from_ftp


class SelectImage(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self._module = None
        self._parent = parent
        self._images = None

        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_margin_top(5)
        self.set_margin_left(5)
        self.set_margin_right(5)
        self.set_margin_bottom(5)

        select_module_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        select_module_label = Gtk.Label(label="Select the module: ")
        select_module_label.set_name("SelectModuleLabel")
        self.select_modules_combobox = Gtk.ComboBoxText()
        self.select_modules_combobox.connect("changed", self.on_module_combo_changed)
        for module in VAR_MODULES:
            self.select_modules_combobox.append_text(module)
        
        select_module_box.pack_start(select_module_label, False, False, 0)
        select_module_box.pack_start(self.select_modules_combobox, True, True, 0)

        self.mid_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
        buttons_box.set_margin_left(200)
        buttons_box.set_margin_right(200)
        self.select_button = Gtk.Button(label="Select")
        self.select_button.connect("clicked", self.on_select_clicked)
        self.select_button.set_sensitive(False)
        self.select_button.set_name("MainButton")
        self.cancel_button = Gtk.Button(label="Cancel")
        self.cancel_button.connect("clicked", self.on_cancel_clicked)
        self.cancel_button.set_name("MainButton")
        buttons_box.pack_start(self.select_button, True, True, 0)
        buttons_box.pack_start(self.cancel_button, True, True, 0)

        self.pack_start(select_module_box, False, False, 0)
        self.pack_start(self.mid_box, True, True, 0)
        self.pack_start(buttons_box, False, False, 0)

    def on_module_combo_changed(self, combo):
        self._module = combo.get_active_text()
        thread = Thread(target=self.recover_image_from_ftp)
        thread.daemon = True
        thread.start()

    def on_select_clicked(self, button):
        self.hide()
        self._parent.main_window.show_all()
        button.set_sensitive(False)
        self._parent.main_window.image_selected()

    def on_cancel_clicked(self, button):
        self.hide()
        self._parent.main_window.show_all()

    def on_select_item_from_tree(self, tree, row, col):
        self._parent.ftp_image = self._images[int(row.to_string())]
        self.select_button.set_sensitive(True)

    def create_tree_view(self):
        images_list = []
        for release in self._images:
            image = []
            image_path = release['Release']['Upload Path']
            image_size = release['Release']['Image Size']
            image.append(os.path.basename(image_path))
            image.append(image_size)
            images_list.append(image)

        store = Gtk.ListStore(str, str)
        for image in images_list:
            store.append(image)

        tree = Gtk.TreeView()
        tree.set_property('activate-on-single-click', True)
        tree.set_model(store)

        rendered_text = Gtk.CellRendererText()
        image_name_column = Gtk.TreeViewColumn(f"{self._module} Images", rendered_text, text=0)
        image_size_column = Gtk.TreeViewColumn(f"Size", rendered_text, text=1)
        tree.append_column(image_name_column)
        tree.append_column(image_size_column)
        tree.connect("row-activated", self.on_select_item_from_tree)

        return tree
    
    def recover_image_from_ftp(self):
        GLib.idle_add(self.select_modules_combobox.set_sensitive, False)
        GLib.idle_add(self.select_button.set_sensitive, False)
        GLib.idle_add(self.cancel_button.set_sensitive, False)

        for child in self.mid_box.get_children():
            GLib.idle_add(self.mid_box.remove, child)

        label = Gtk.Label(label="Retrieving available images from the FTP...")
        label.set_name("SelectModuleLabel")
        GLib.idle_add(self.mid_box.pack_start, label, True, True, 0)
        GLib.idle_add(self.mid_box.show_all)

        self._images = get_images_list_from_ftp(self._module)

        GLib.idle_add(self.mid_box.remove, label)

        tree = self.create_tree_view()
        GLib.idle_add(self.mid_box.pack_start, tree, True, True, 0)
        GLib.idle_add(self.mid_box.show_all)

        GLib.idle_add(self.select_modules_combobox.set_sensitive, True)
        GLib.idle_add(self.cancel_button.set_sensitive, True)
