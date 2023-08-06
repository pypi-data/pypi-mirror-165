# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from re import L
import gi
gi.require_version('Gtk', "3.0")
from gi.repository import GLib, Gtk
import ftplib
import os
from subprocess import Popen, PIPE
from threading import Thread

from writer.config import CACHEDIR
from writer.ftp import connect_ftp
from writer.utils import is_gzipped, get_file_size, get_gzipped_file_size


class FlashImage(Gtk.Box):
    def __init__(self, parent, ftp=False):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self._parent = parent
        self._image = self._parent.ftp_image if ftp else parent.local_image
        self._device = self._parent.device

        self.set_homogeneous(False)
        self.set_hexpand(True)
        self.set_margin_top(150)
        self.set_margin_left(100)
        self.set_margin_right(100)
        self.set_margin_bottom(150)

        self.progress_label = Gtk.Label()
        self.progress_label.set_name("SelectModuleLabel")
        self.pack_start(self.progress_label, False, False, 0)

        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_text("0%")
        self.progress_bar.set_show_text(True)
        self.pack_start(self.progress_bar, False, False, 0)

    def on_finish_button_clicked(self, button):
        self.hide()
        self._parent.main_window.show_all()
        self._parent.main_window.on_cancel_image_clicked(self.finish_button)

    def download_image_from_ftp(self):
        remote_path, file_name = os.path.split(self._image['Release']['Upload Path'])
        file_size = get_file_size(self._image['Release']['Image Size'])
        local_file = os.path.join(CACHEDIR, file_name)
        if os.path.exists(local_file):
            os.remove(local_file)
        ftp, err = connect_ftp("customerv", "Variscite1")
        if not err:
            try:
                GLib.idle_add(self.progress_label.set_text,
                              f"Downloading {file_name} from the FTP")
                ftp.cwd(remote_path)
                with open(local_file, "wb") as file_obj:
                    global total
                    total = 0
                    def file_write(data):
                        global total
                        total += len(data)
                        frac = total / file_size
                        GLib.idle_add(self.progress_bar.set_fraction, frac)
                        GLib.idle_add(self.progress_bar.set_text, f"{(frac * 100):.2f}%")
                        file_obj.write(data)

                    res = ftp.retrbinary(f"RETR {file_name}", file_write, blocksize=8192)
                    if not res.startswith("226 Transfer complete"):
                        os.remove(local_file)
                        return False
            except ftplib.all_errors as error:
                ftp.quit()
                return False
            ftp.quit()
            return local_file
        return False

    def flash_local_image(self):
        thread = Thread(target=self.flash_image, args=(self._image,))
        thread.daemon = True
        thread.start()

    def flash_ftp_image(self):
            thread = Thread(target=self.download_and_flash)
            thread.daemon = True
            thread.start()

    def download_and_flash(self):
        local_image_path = os.path.join(CACHEDIR, os.path.basename(self._image['Release']['Upload Path']))
        if os.path.exists(local_image_path):
            self._image_path = local_image_path
        else:
            self._image_path = self.download_image_from_ftp()

        self.flash_image(self._image_path)

    def flash_image(self, image_path):
        if is_gzipped(image_path):
            GLib.idle_add(self.progress_label.set_text,
                          "Calculating decompressed image size...")
            self.set_spinner()
            image_size = get_gzipped_file_size(image_path)
            GLib.idle_add(self.remove, self.spinner)
            self.progress_bar = Gtk.ProgressBar()
            GLib.idle_add(self.progress_bar.set_text, "0%")
            GLib.idle_add(self.progress_bar.set_show_text, True)
            GLib.idle_add(self.pack_start, self.progress_bar, False, False, 0)
            GLib.idle_add(self.show_all)
        else:
            image_stat = os.stat(image_path)
            image_size = image_stat.st_size

        cmd = f"pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY external_writer_var " \
              f"{image_path} {image_size} {self._device}"
        self.write_proc = Popen([cmd], shell=True, stdout=PIPE, bufsize=0)

        GLib.idle_add(self.progress_label.set_text,
                      f"Flashing {os.path.basename(image_path)} to {self._device}")
        GLib.io_add_watch(self.write_proc.stdout, GLib.PRIORITY_DEFAULT,
                          GLib.IO_IN | GLib.IO_HUP, self.update_pb)

    def update_pb(self, stdout, flags):
        if flags & GLib.IO_HUP:
            self.write_proc.wait()
            GLib.idle_add(self.progress_label.set_text,
                          "Completed. You can safely remove your device.")
            GLib.idle_add(self.spinner.stop)
            self.finish_button = Gtk.Button.new_with_label("Finish")
            self.finish_button.set_name("MainButton")
            self.finish_button.connect("clicked", self.on_finish_button_clicked)
            GLib.idle_add(self.pack_start, self.finish_button, False, False, 0)
            GLib.idle_add(self.show_all)
            return False

        line = stdout.readline().decode()
        bytes_progress = line.split('/')
        if len(bytes_progress) > 1:
            frac = (100 * int(bytes_progress[0])) // int(bytes_progress[1])
            GLib.idle_add(self.progress_bar.set_fraction, (frac / 100))
            GLib.idle_add(self.progress_bar.set_text, f"{frac}%")
        else:
            GLib.idle_add(self.progress_label.set_text, bytes_progress[0])
            self.set_spinner()

        return True

    def set_spinner(self):
        GLib.idle_add(self.remove, self.progress_bar)
        self.spinner = Gtk.Spinner()
        GLib.idle_add(self.spinner.start)
        GLib.idle_add(self.pack_start, self.spinner, True, True, 0)
        GLib.idle_add(self.show_all)
