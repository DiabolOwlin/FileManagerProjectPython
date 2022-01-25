import tkinter
from MainContext import *
from FileContext import *
from DirContext import *


class MainWindow:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("FileManager")
        self.root.resizable(width=False, height=False)
        self.root.geometry('450x300')

        self.hidden_dir = tkinter.IntVar()
        self.buff = None
        self.all_program = os.listdir('/')
        # self.all_program = os.listdir('/')

        self.root.bind('<Button-1>', self.root_click)
        self.root.bind('<FocusOut>', self.root_click)

        # top frame
        self.title_frame = tkinter.Frame(self.root)
        self.title_frame.pack(fill='both', expand=True)

        # back button
        self.back_button = tkinter.Button(self.title_frame, text="..", command=self.parent_dir, width=1, height=1)
        self.back_button.pack(side='left')

        # path entry
        self.path_text = tkinter.StringVar()
        self.path_text.set('/')
        self.current_path = tkinter.Entry(self.title_frame, textvariable=self.path_text, width=40, state='readonly')
        self.current_path.pack(side='left')

        # button show/hidde hidden dir/file
        self.check_button = tkinter.Checkbutton(self.title_frame, text="Hidden", font=("Helvetica", 10), padx=1, pady=1,
                                                variable=self.hidden_dir, command=self.refresh_window)
        self.check_button.pack(side='left')

        # main frame
        self.main_frame = tkinter.Frame(self.root)
        self.main_frame.pack()

        # scroll bar
        self.scrollbar_vert = tkinter.Scrollbar(self.main_frame, orient="vertical")
        self.scrollbar_vert.pack(side='right', fill='y')

        self.scrollbar_hor = tkinter.Scrollbar(self.main_frame, orient="horizontal")
        self.scrollbar_hor.pack(side='bottom', fill='x')

        # canvas
        self.canvas = tkinter.Canvas(self.main_frame, borderwidth=0, bg='white')
        self.inner_frame = tkinter.Frame(self.canvas, bg='white')

        # scroll commands
        self.scrollbar_vert["command"] = self.canvas.yview
        self.scrollbar_hor["command"] = self.canvas.xview

        # canvas settings
        self.canvas.configure(yscrollcommand=self.scrollbar_vert.set,
                              xscrollcommand=self.scrollbar_hor.set, width=400,
                              heigh=250)

        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # draw the contents of the directory
        self.dir_content()

    def root_click(self, event):
        # if other menus are active - canceling those
        if self.file_context_menu:
            self.file_context_menu.unpost()
        if self.main_context_menu:
            self.main_context_menu.unpost()
        if self.dir_context_menu:
            self.dir_context_menu.unpost()

    def dir_content(self):
        # content in current directory
        dir_list = os.listdir(self.path_text.get())
        path = self.path_text.get()

        if not dir_list:
            # main context menu

            self.main_context_menu = MainContextMenu(self, self.canvas)
            self.canvas.bind('<Button-3>', self.main_context_menu.popup_menu)
            if self.buff:
                self.main_context_menu.add_command(label="Insert", command=self.main_context_menu.insert_to_dir)
            self.inner_frame.bind('<Button-3>', self.main_context_menu.popup_menu)
            # file context menu
            self.file_context_menu = None
            # directory context menu
            self.dir_context_menu = None
            return None

        # main context menu
        self.main_context_menu = MainContextMenu(self, self.canvas)
        self.canvas.bind('<Button-3>', self.main_context_menu.popup_menu)

        if self.buff:
            self.main_context_menu.add_command(label="Insert", command=self.main_context_menu.insert_to_dir)

        # file context menu
        self.file_context_menu = FileContextMenu(self, self.inner_frame)

        # directory context menu
        self.dir_context_menu = DirContextMenu(self, self.inner_frame)

        i = 0
        for item in dir_list:

            if os.path.isdir(str(path) + item):

                # processing directories
                if os.access(str(path) + item, os.R_OK):
                    if (not self.hidden_dir.get() and not item.startswith('.')) or self.hidden_dir.get():
                        photo = tkinter.PhotoImage(file="img/folder.png")

                        icon = tkinter.Label(self.inner_frame, image=photo, bg='white')
                        icon.image = photo
                        icon.grid(row=i + 1, column=0)

                        folder_name = tkinter.Label(self.inner_frame, text=item, bg='white', cursor='hand1')
                        folder_name.bind("<Button-1>", self.move_to_dir)
                        folder_name.bind("<Button-3>", self.dir_context_menu.popup_menu)
                        folder_name.grid(row=i + 1, column=1, sticky='w')
                else:
                    if (not self.hidden_dir.get() and not item.startswith('.')) or self.hidden_dir.get():
                        photo = tkinter.PhotoImage(file="img/folder_access.png")

                        icon = tkinter.Label(self.inner_frame, image=photo, bg='white')
                        icon.image = photo
                        icon.grid(row=i + 1, column=0)

                        folder_name = tkinter.Label(self.inner_frame, text=item, bg='white')
                        folder_name.bind("<Button-1>", self.move_to_dir)
                        folder_name.grid(row=i + 1, column=1, sticky='w')

            else:
                # processing files
                if (not self.hidden_dir.get() and not item.startswith('.')) or self.hidden_dir.get():
                    ext = self.take_extention_file(item)
                    # photos, images
                    if ext in ['jpeg', 'jpg', 'png', 'gif']:
                        photo = tkinter.PhotoImage(file="img/photo.png")

                        icon = tkinter.Label(self.inner_frame, image=photo, bg='white')
                        icon.image = photo
                        icon.grid(row=i + 1, column=0)

                        file_name = tkinter.Label(self.inner_frame, text=item, bg='white')
                        file_name.grid(row=i + 1, column=1, sticky='w')

                        file_name.bind("<Button-3>", self.file_context_menu.popup_menu)
                    else:
                        # other files
                        if os.access(str(path) + item, os.R_OK):
                            photo = tkinter.PhotoImage(file="img/file.png")

                            icon = tkinter.Label(self.inner_frame, image=photo, bg='white')
                            icon.image = photo
                            icon.grid(row=i + 1, column=0)

                            folder_name = tkinter.Label(self.inner_frame, text=item, bg='white')
                            folder_name.grid(row=i + 1, column=1, sticky='w')

                            folder_name.bind("<Button-3>", self.file_context_menu.popup_menu)

                        else:
                            photo = tkinter.PhotoImage(file="img/file_access.png")

                            icon = tkinter.Label(self.inner_frame, image=photo, bg='white')
                            icon.image = photo
                            icon.grid(row=i + 1, column=0)

                            folder_name = tkinter.Label(self.inner_frame, text=item, bg='white')
                            folder_name.grid(row=i + 1, column=1, sticky='w')
            i += 1
        # updating inner_frame and placing scrollbar for new content
        self.inner_frame.update()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def move_to_dir(self, event):
        elem = event.widget
        dir_name = elem["text"]
        fool_path = self.path_text.get() + dir_name
        if os.path.isdir(fool_path) and os.access(fool_path, os.R_OK):
            old_path = self.path_text.get()
            self.path_text.set(old_path + dir_name + '/')
            self.root_click('<Button-1>')
            self.refresh_window()

    def parent_dir(self):
        old_path = [i for i in self.path_text.get().split('/') if i]
        new_path = '/' + '/'.join(old_path[:-1])
        if not new_path:
            new_path = '/'
        if os.path.isdir(new_path):
            if new_path == '/':
                self.path_text.set(new_path)

            else:
                self.path_text.set(new_path + '/')
            self.refresh_window()

    @staticmethod
    def take_extention_file(file_name):

        ls = file_name.split('.')
        if len(ls) > 1:
            return ls[-1]
        else:
            return None

    def refresh_window(self):

        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.dir_content()
        self.canvas.yview_moveto(0)


win = MainWindow()
win.root.mainloop()
