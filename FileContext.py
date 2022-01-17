import tkinter
import subprocess
from tkinter import messagebox
from tkinter import simpledialog


class FileContextMenu(tkinter.Menu):
    def __init__(self, main_window, parent):
        super(FileContextMenu, self).__init__(parent, tearoff=0)
        self.main_window = main_window
        self.add_command(label="Open", command=self.open_file)
        self.add_separator()
        self.add_command(label="Copy", command=self.copy_file)
        self.add_command(label="Rename", command=self.rename_file)
        self.add_separator()
        self.add_command(label="Delete", command=self.delete_file)

    def open_file(self):
        ''' open files with other programs method '''
        ext = self.main_window.take_extention_file(self.main_window.selected_file)
        full_path = self.main_window.path_text.get() + self.main_window.selected_file

        if ext in ['txt', 'py', 'html', 'css', 'js']:
            if 'mousepad' in self.main_window.all_program:
                subprocess.Popen(["mousepad", full_path], shell=True, start_new_session=True)
            else:
                self.problem_message()
        elif ext == 'pdf':
            if 'evince' in self.main_window.all_program:
                subprocess.run(["evince", full_path], shell=True, start_new_session=True)
            else:
                self.problem_message()
        elif ext in ['png', 'jpeg', 'jpg', 'gif']:
            if 'ristretto' in self.main_window.all_program:
                subprocess.run(["ristretto", full_path], shell=True, start_new_session=True)
            else:
                self.problem_message()
        else:
            self.problem_message()

    def problem_message(self):
        messagebox.showwarning("Problem with opening the file", 'You cannot open this file!')

    def copy_file(self):
        # place full path to buffer
        self.main_window.buff = self.main_window.path_text.get() + self.main_window.selected_file
        self.main_window.refresh_window()

    def delete_file(self):
        full_path = self.main_window.path_text.get() + self.main_window.selected_file

        # executing command with separate process
        process = subprocess.Popen(['rm', full_path], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = process.communicate()

        # if error occurred
        if err:
            messagebox.showwarning("Problem with deleting the file", 'You have no rights to delete this file!')
        self.main_window.refresh_window()

    def rename_file(self):
        new_name = simpledialog.askstring("Rename File", "Enter new name")

        if new_name:
            old_file = self.main_window.path_text.get() + self.main_window.selected_file
            new_file = self.main_window.path_text.get() + new_name

            # executing command with separate process
            process = subprocess.Popen(['mv', old_file, new_file], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = process.communicate()

            # if error occurred
            if err:
                messagebox.showwarning("Problem with renaming the file",
                                       'You have no rights to rename this file!')
            self.main_window.refresh_window()

    def popup_menu(self, event):
        self.post(event.x_root, event.y_root)

        # if other menus are active - canceling those

        if self.main_window.main_context_menu:
            self.main_window.main_context_menu.unpost()

        if self.main_window.dir_context_menu:
            self.main_window.dir_context_menu.unpost()

        self.main_window.selected_file = event.widget["text"]