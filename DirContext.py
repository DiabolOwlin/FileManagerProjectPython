import tkinter as tk
import os
import subprocess
from tkinter import messagebox
from tkinter import simpledialog


class DirContextMenu(tk.Menu):
    def __init__(self, main_window, parent):
        super(DirContextMenu, self).__init__(parent, tearoff=0)
        self.main_window = main_window
        self.add_command(label="Rename", command=self.rename_dir)
        self.add_command(label="Copy", command=self.copy_dir)
        self.add_separator()
        self.add_command(label="Delete", command=self.delete_dir)

    def copy_dir(self):
        self.main_window.buff = self.main_window.path_text.get() + self.main_window.selected_file
        self.main_window.refresh_window()

    def delete_dir(self):
        cmd = "rm"
        full_path = self.main_window.path_text.get() + self.main_window.selected_file
        # print(full_path)
        if os.path.isdir(full_path):

            # executing command with separate process
            process = subprocess.Popen(['rm', '-rf', full_path], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = process.communicate()

            print(output)
            print(err)
            # del full_path
            # if error occurred
            if err:
                messagebox.showwarning("Problem with deleting the directory",
                                       'You have no rights to delete this directory!')
        self.main_window.refresh_window()

    def rename_dir(self):
        new_name = simpledialog.askstring("Rename directory", "Enter new name")
        if new_name:
            old_dir = self.main_window.path_text.get() + self.main_window.selected_file
            new_dir = self.main_window.path_text.get() + new_name

            # executing command with separate process
            process = subprocess.Popen(['mv', old_dir, new_dir], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = process.communicate()
            print(output)
            print(err)
            # if error occurred
            if err:
                messagebox.showwarning("Problem with renaming the directory",
                                       'You have no rights to rename this directory!')
            self.main_window.refresh_window()

    def popup_menu(self, event):
        ''' "activate context menu" method '''
        self.post(event.x_root, event.y_root)

        # if other menus are active - canceling those
        if self.main_window.main_context_menu:
            self.main_window.main_context_menu.unpost()

        if self.main_window.file_context_menu:
            self.main_window.file_context_menu.unpost()
        self.main_window.selected_file = event.widget["text"]