import tkinter
import os
import subprocess
from tkinter import messagebox
from tkinter import simpledialog


class MainContextMenu(tkinter.Menu):

    def __init__(self, main_window, parent):
        super(MainContextMenu, self).__init__(parent, tearoff=0)
        self.main_window = main_window
        self.add_command(label="Create directory", command=self.create_dir)
        self.add_command(label="Create file", command=self.create_file)

    def popup_menu(self, event):
        ''' "activate context menu" method'''

        # if other menus are active - canceling those
        if self.main_window.file_context_menu:
            self.main_window.file_context_menu.unpost()

        if self.main_window.dir_context_menu:
            self.main_window.dir_context_menu.unpost()
        self.post(event.x_root, event.y_root)

    def create_dir(self):

        dir_name = simpledialog.askstring("New directory", "Enter name of a directory")
        if dir_name:
            command = "mkdir {0}".format(dir_name).split(' ')

            # executing command with separate process
            process = subprocess.Popen(command, cwd=self.main_window.path_text.get(), stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            out, err = process.communicate()

            # if error occurred
            if err:
                messagebox.showwarning("Operation is not possible!", "Access denied!")
            self.main_window.refresh_window()

    def create_file(self):
        dir_name = simpledialog.askstring("New file", "Enter name of a file")
        if dir_name:
            command = "touch {0}".format(dir_name).split(' ')

            # executing command with separate process
            process = subprocess.Popen(command, cwd=self.main_window.path_text.get(), stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            out, err = process.communicate()

            # if error occurred
            if err:
                messagebox.showwarning("Operation is not possible!", "Access denied!")
            self.main_window.refresh_window()

    def insert_to_dir(self):
        ''' "copy file or directory into current directory" method '''
        copy_obj = self.main_window.buff
        to_dir = self.main_window.path_text.get()
        if os.path.isdir(self.main_window.buff):

            # executing command with separate process
            process = subprocess.Popen(['cp', '-r', copy_obj, to_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()

            # if error occurred
            if err:
                messagebox.showwarning("Operation is not possible!", err.decode("utf-8"))
        else:
            # executing command with separate process
            process = subprocess.Popen(['cp', '-n', copy_obj, to_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()

            # if error occurred
            if err:
                messagebox.showwarning("Operation is not possible!", err.decode("utf-8"))
        self.main_window.refresh_window()
