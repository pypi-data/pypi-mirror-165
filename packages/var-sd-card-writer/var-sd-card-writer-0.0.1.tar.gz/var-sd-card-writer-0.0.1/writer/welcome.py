# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from re import L
import gi
gi.require_versions({'GdkPixbuf': "2.0", 'Gtk': "3.0"})
from gi.repository import GdkPixbuf, Gtk
import os

from writer.config import CACHEDIR
from writer.flasher import FlashImage
from writer.device import query_disk_devices
from writer.utils import get_readable_size


class MainWindow(Gtk.Box):
    def __init__(self, parent):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self._parent = parent

        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_margin_top(10)
        self.set_margin_left(10)
        self.set_margin_right(10)
        self.set_margin_bottom(10)

        image = Gtk.Image()
        logo = GdkPixbuf.Pixbuf.new_from_file(os.path.join(CACHEDIR, "assets", "variscite.png"))
        image.set_from_pixbuf(logo)

        buttons_box = Gtk.Box()
        buttons_grid = Gtk.Grid()
        buttons_grid.set_hexpand(True)
        buttons_grid.set_row_spacing(10)
        buttons_grid.set_row_homogeneous(True)
        buttons_grid.set_column_spacing(10)
        buttons_grid.set_column_homogeneous(True)
        buttons_box.pack_start(buttons_grid, True, False, 0)

        self.local_image_button = Gtk.Button.new()
        self.local_image_button.add(self.create_icon_button("computer", "Select Local Image"))
        self.local_image_button.connect("clicked", self.on_local_image_clicked)
        self.local_image_button.set_name("MainButton")
        self.ftp_image_button = Gtk.Button.new()
        self.ftp_image_button.add(self.create_icon_button("weather-overcast",
                                                          "Select Image from FTP"))
        self.ftp_image_button.connect("clicked", self.on_ftp_image_clicked)
        self.ftp_image_button.set_name("MainButton")
        self.select_device_button = Gtk.Button.new()
        self.select_device_button.add(self.create_icon_button("media-removable",
                                                              "Select a USB Drive"))
        self.select_device_button.connect("clicked", self.on_select_device_clicked)
        self.select_device_button.set_sensitive(False)
        self.select_device_button.set_name("MainButton")
        self.flash_image_button = Gtk.Button.new()
        self.flash_image_button.add(self.create_icon_button("media-flash",
                                                            "Flash Image"))
        self.flash_image_button.connect("clicked", self.on_flash_image_clicked)
        self.flash_image_button.set_sensitive(False)
        self.flash_image_button.set_name("MainButton")

        buttons_grid.attach(self.local_image_button, 0, 0, 1, 1)
        buttons_grid.attach(self.ftp_image_button, 0, 1, 1, 1)
        buttons_grid.attach(self.select_device_button, 1, 0, 1, 1)
        buttons_grid.attach(self.flash_image_button, 2, 0, 1, 1)

        self.selected_grid = Gtk.Grid()
        self.selected_grid.set_hexpand(True)
        self.selected_grid.set_row_spacing(10)
        self.selected_grid.set_row_homogeneous(True)
        self.selected_grid.set_column_spacing(10)
        self.selected_grid.set_column_homogeneous(True)

        self.pack_start(image, False, False, 0)
        self.pack_start(buttons_box, True, False, 0)
        self.pack_start(self.selected_grid, False, False, 0)

    def on_local_image_clicked(self, button):
        dialog = Gtk.FileChooserDialog(title="Please choose a file", parent=self._parent,
                                       action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            image = dialog.get_filename()
            self._parent.local_image = image
            self.image_selected(ftp=False)

        dialog.destroy()

    def on_ftp_image_clicked(self, button):
        self.hide()
        self._parent.ftp_image_window.show_all()

    def on_select_device_clicked(self, button):
        disks = query_disk_devices(False)
        for disk in disks:
            if disks[disk]['size'] < 100000000000:
                disk_info = []
                disk_info.append(str(disk))
                disk_info.append(str(get_readable_size(disks[disk]['size'])))
                disk_info.append(str(disks[disk]['model']))

                if disk_info not in self._parent.devices:
                    self._parent.devices.append(disk_info)

        dialog = SelectDeviceDialog(self._parent)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self._parent.device = dialog.device
            self.device_selected()
        elif response == Gtk.ResponseType.CANCEL:
            self.select_device_button.set_sensitive(True)
            self._parent.device = None

        dialog.destroy()

    def on_flash_image_clicked(self, button):
        if self._parent.local_image:
            self.flash_local_image()
        elif self._parent.ftp_image:
            self.flash_ftp_image()

    def flash_local_image(self):
        self.hide()
        self._parent.main_container.remove(self._parent.flash_image_window)
        self._parent.flash_image_window = FlashImage(self._parent)
        self._parent.main_container.add(self._parent.flash_image_window)
        self._parent.flash_image_window.show_all()
        self._parent.flash_image_window.flash_local_image()

    def flash_ftp_image(self):
        self.hide()
        self._parent.main_container.remove(self._parent.flash_image_window)
        self._parent.flash_image_window = FlashImage(self._parent, ftp=True)
        self._parent.main_container.add(self._parent.flash_image_window)
        self._parent.flash_image_window.show_all()
        self._parent.flash_image_window.flash_ftp_image()

    def on_cancel_image_clicked(self, button):
        self._parent.local_image = None
        self._parent.ftp_image = None
        self.local_image_button.set_sensitive(True)
        self.ftp_image_button.set_sensitive(True)
        self.select_device_button.set_sensitive(False)
        self.flash_image_button.set_sensitive(False)

        for child in self.selected_grid.get_children():
            self.selected_grid.remove(child)

        self.selected_grid.show_all()

    def on_change_drive_clicked(self, button):
        self.selected_grid.remove_row(1)
        self.selected_grid.show_all()
        self.on_select_device_clicked(self.select_device_button)

    def create_icon_button(self, icon_name, label_name):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        icon_theme = Gtk.IconTheme.get_default()
        icon = icon_theme.load_icon(icon_name, -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        label = Gtk.Label.new_with_mnemonic(label_name)
        hbox.pack_start(image, False, False, 0)
        hbox.pack_start(label, True, True, 0)

        return hbox

    def image_selected(self, ftp=True):
        self.local_image_button.set_sensitive(False)
        self.ftp_image_button.set_sensitive(False)
        self.select_device_button.set_sensitive(True)

        if ftp:
            image = os.path.basename(self._parent.ftp_image['Release']['Upload Path'])
        else:
            image = self._parent.local_image
    
        label = Gtk.Label(label=f"Selected image: {os.path.basename(image)}")
        button = Gtk.Button.new_with_label("Cancel")
        button.connect("clicked", self.on_cancel_image_clicked)
        button.set_name("MainButton")

        self.selected_grid.attach(label, 0, 0, 3, 1)
        self.selected_grid.attach(button, 3, 0, 1, 1)
        self.selected_grid.show_all()

    def device_selected(self):
        self.select_device_button.set_sensitive(False)
        self.flash_image_button.set_sensitive(True)

        label = Gtk.Label(label=f"Selected device: {self._parent.device}")
        button = Gtk.Button.new_with_label("Change")
        button.connect("clicked", self.on_change_drive_clicked)
        button.set_name("MainButton")

        self.selected_grid.attach(label, 0, 1, 3, 1)
        self.selected_grid.attach(button, 3, 1, 1, 1)
        self.selected_grid.show_all()


class SelectDeviceDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Select a USB Drive", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OK, Gtk.ResponseType.OK)

        self.set_default_size(640, 480)
        self.device = None

        box = self.get_content_area()

        if parent.devices:
            tree = self.create_tree_view(parent.devices)
            model = tree.get_model()
            self.device = model[0][0]
            box.add(tree)
        else:
            label = Gtk.Label("No device found")
            box.add(label)

        self.show_all()

    def on_select_item_from_tree(self, tree, row, col):
        model = tree.get_model()
        self.device = model[row][0]

    def create_tree_view(self, devices_list):
        store = Gtk.ListStore(str, str, str)
        for device in devices_list:
            store.append(device)

        tree = Gtk.TreeView()
        tree.set_property('activate-on-single-click', True)
        tree.set_model(store)

        rendered_text = Gtk.CellRendererText()
        device_name_column = Gtk.TreeViewColumn(f"Device", rendered_text, text=0)
        device_size_column = Gtk.TreeViewColumn(f"Size", rendered_text, text=1)
        device_model_column = Gtk.TreeViewColumn(f"Model", rendered_text, text=2)
        tree.append_column(device_name_column)
        tree.append_column(device_size_column)
        tree.append_column(device_model_column)
        tree.connect("row-activated", self.on_select_item_from_tree)

        return tree
