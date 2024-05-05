import customtkinter as ctk
from customtkinter import CTkEntry, CTkLabel, CTkTextbox

from assets import BTN_FS, FONTS


class KernelFrame(ctk.CTkFrame):
    def __init__(self, master, width, kernel_size, **args):
        super().__init__(master, width=width, **args)
        self.grid(row=0, column=0)
        self.super = master
        self.width = width
        self.kernel_size = kernel_size
        self.kernel_entries = []
        self.update_kernel(kernel_size)
        self.old_value = [entry.get() for entry in self.kernel_entries]

    def update_kernel(self, kernel_size):
        self.kernel_size = kernel_size

        hw = int({"3": 50, "5": 36, "7": 26}[str(kernel_size)])
        self.clear_kernel()
        for row in range(kernel_size):
            for col in range(kernel_size):
                font = ctk.CTkFont(family=FONTS['Arial'], weight="bold",
                                   size=int({"3": 15, "5": 12, "7": 8}[str(kernel_size)]))
                entry = CTkEntry(self, width=hw, height=hw, justify='center', font=font)
                entry.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
                entry.insert(0, "0")
                entry.bind("<KeyRelease>", self.entry_changed)
                self.kernel_entries.append(entry)

    def clear_kernel(self):
        for entry in self.kernel_entries:
            entry.grid_forget()
            entry.destroy()
        self.kernel_entries.clear()

    def entry_changed(self, event):
        import re
        print("event:", event)
        for i, entry in enumerate(self.kernel_entries):
            e = entry.get()
            if not re.match(r'^[0-9./-]+$', e):
                entry.delete(0, "end")
                if e != "":
                    entry.insert(0, self.old_value[i])

        self.old_value = [entry.get() for entry in self.kernel_entries]
        print(f"Entry values: {self.old_value}")

    def get_kernel(self):
        import numpy as np
        values = []
        for entry in self.kernel_entries:
            e = entry.get()
            if e.__contains__("/"):
                e = eval(e)
            if e == "":
                e = 0
            values.append(float(e))
        values = np.reshape(values, (self.kernel_size, self.kernel_size))
        return values


class KernelConfigurator(ctk.CTkFrame):
    def __init__(self, master, frame_root, width=100, **kwargs):
        super().__init__(frame_root, width=width, corner_radius=0, **kwargs)
        self.name_id = "kernel conf class"
        self.parent = master
        self.pack(fill="both", expand=True, side="top")
        self.grid_columnconfigure(1, weight=1)  # Allow the first column to expand

        self.kernel_size = 3
        row = 0
        # Menu for kernel size
        font_conf = ctk.CTkFont(family=FONTS['Montserrat'], weight="bold", size=BTN_FS)

        self.label_kernel_size = CTkLabel(self, text="kernel size:", justify="left")
        self.label_kernel_size.grid(row=row, column=1, padx=(5, 0), columnspan=self.kernel_size - 1, pady=(5, 5),
                                    )
        self.label_kernel_size.configure(font=font_conf)

        self.kernel_size_menu = ctk.CTkOptionMenu(self, fg_color="gray", button_color="#5a00aa",
                                                  values=["3", "5", "7"], width=50,
                                                  command=self.set_kernel_size)
        self.kernel_size_menu.grid(row=row, column=self.kernel_size, padx=5, pady=(0, 5))
        self.kernel_size_menu.configure(font=font_conf)
        self.kernel_size_menu.set("3")
        row += 1

        # Grid of entries for the kernel
        self.kernel_grid = KernelFrame(self, width=width, kernel_size=self.kernel_size)
        self.kernel_grid.grid(row=row, column=1, columnspan=self.kernel_size, padx=1, pady=(10, 0))
        row += 1

        # apply_conv Button
        self.apply_conv = ctk.CTkButton(self, text="Apply the convolution".title(), fg_color="#042d64",
                                        corner_radius=10, border_spacing=1,
                                        border_color="#3a596d", border_width=1, height=35,
                                        command=self.apply_conv)

        self.apply_conv.grid(row=row, column=1, columnspan=self.kernel_size, padx=10, pady=(20, 0))
        self.apply_conv.configure(font=ctk.CTkFont(family=FONTS['Montserrat'], weight="bold", size=BTN_FS))

        row += 1

        # ttk.Separator(self, orient='horizontal').grid(row=row, column=1,,
        #                                               sticky='ew', )

        # progressbar
        self.progressbar = self.create_progressbar(col=1, row=row, pad_y=(10, 20), column_span=self.kernel_size)
        self.progressbar_row = row
        row += 1

        # padding label
        self.label_padding = CTkLabel(self, text="Padding:", justify="left")
        self.label_padding.grid(row=row, column=1, padx=(5, 0), columnspan=self.kernel_size - 1, pady=(1, 5),
                                sticky="w")
        self.label_padding.configure(font=font_conf)
        # Padding entry
        self.padding_entry = CTkEntry(self, width=40)
        self.padding_entry.grid(row=row, column=self.kernel_size, columnspan=self.kernel_size - 1, padx=5, sticky="ew")
        self.padding_entry.insert(0, "0")
        row += 1

        # Stride label
        self.label_Stride = CTkLabel(self, text="Stride:", justify="left")
        self.label_Stride.grid(row=row, column=1, padx=(5, 0), columnspan=self.kernel_size - 1, pady=(1, 5),
                               sticky="w")
        self.label_Stride.configure(font=font_conf)
        # Stride entry
        self.stride_entry = CTkEntry(self, width=40)
        self.stride_entry.grid(row=row, column=self.kernel_size, columnspan=self.kernel_size - 1, padx=5, sticky="ew")
        self.stride_entry.insert(0, "1")
        row += 1

        # args label
        self.label_args = CTkLabel(self, text="arguments :", justify="left")
        self.label_args.grid(row=row, column=1, padx=(5, 0), columnspan=self.kernel_size, pady=(1, 5), sticky="w")
        self.label_args.configure(font=font_conf)
        row += 1
        # Additional arguments entry
        self.args_textbox = CTkTextbox(self, height=10, font=font_conf, border_spacing=25)
        self.args_textbox.grid(row=row, sticky="news", column=1, columnspan=self.kernel_size, padx=1,
                               pady=(0, 10))

        self.args_textbox_placeholder = "use this format:\narg1=value1\narg2=value2\narg3=value3\n...."
        self.args_textbox.insert("0.0", self.args_textbox_placeholder)
        self.args_textbox.bind("<FocusIn>", self.clear_placeholder)

        # Make the last row expandable
        self.rowconfigure(row, weight=1)

    def clear_placeholder(self, event):
        print("clear_placeholder event", event)
        if self.args_textbox.get("0.0", "end-1c") == self.args_textbox_placeholder:
            self.args_textbox.delete("0.0", "end")

    def set_kernel_size(self, size):
        self.kernel_size = size
        self.kernel_grid.update_kernel(int(size))

        print("kernel_size is ", self.kernel_size)
        print(self.winfo_width())

    def apply_conv(self):
        import threading
        import numpy as np
        
        def conv():
            self.progressbar.configure(fg_color="#121e4c")
            self.progressbar.start()
            self.parent.apply_convolution(kernel=np.array(self.kernel_grid.get_kernel()),
                                          stride=int(self.stride_entry.get()),
                                          padding=int(self.padding_entry.get()))

            self.progressbar.stop()
            # progressbar
            progressbar = self.create_progressbar(row=self.progressbar_row, col=1,
                                                  pad_y=(10, 20), column_span=self.kernel_size)
            self.progressbar.destroy()
            self.progressbar = progressbar

        def start_progressbar():
            self.progressbar.start()

        t1 = threading.Thread(target=conv)
        t2 = threading.Thread(target=start_progressbar)

        # Start threads
        t1.start()
        t2.start()

        print(self.name_id, "apply convolution ended")

    def create_progressbar(self, col, row, pad_y, column_span):
        progressbar = ctk.CTkProgressBar(self, mode="indeterminate", height=5,
                                         fg_color="#f1f1f1", progress_color="#f1f1f1")
        progressbar.grid(row=row, column=col, columnspan=column_span, padx=1, sticky='ew', pady=pad_y)
        return progressbar


class FilterConfigurator(ctk.CTkFrame):
    def __init__(self, master, frame_root, width=100, **kwargs):
        super().__init__(frame_root, width=width, corner_radius=0, **kwargs)

        self.name_id = "filter config class"
        self.parent = master
        self.pack(fill="both", expand=True, side="top")
        self.grid_columnconfigure(1, weight=1)  # Allow the first column to expand

        self.kernel_size = 3
        row = 0

        font_conf = ctk.CTkFont(family=FONTS['Montserrat'], weight="bold", size=BTN_FS)

        # Menu for kernel size
        self.label_kernel_size = CTkLabel(self, text="kernel size:", justify="left")
        self.label_kernel_size.grid(row=row, column=1, padx=(5, 0), pady=(5, 5),
                                    )
        self.label_kernel_size.configure(font=font_conf)

        self.kernel_size_menu = ctk.CTkOptionMenu(self, fg_color="gray", button_color="#5a00aa",
                                                  values=["3", "5", "7"], width=50,
                                                  command=self.set_kernel_size)
        self.kernel_size_menu.grid(row=row, column=2, padx=5, pady=(0, 5))
        self.kernel_size_menu.configure(font=font_conf)
        self.kernel_size_menu.set("3")
        row += 1

        # filter menu
        self.filters: dict = self.get_filters()
        self.label_filter_option = CTkLabel(self, text="select filter:", justify="center")
        self.label_filter_option.grid(row=row, column=1, padx=(5, 0), pady=(1, 5),
                                      columnspan=2)
        self.label_filter_option.configure(font=font_conf)
        row += 1
        self.filter_option_menu = ctk.CTkOptionMenu(self, values=list(sorted(self.filters.keys())),
                                                    button_color="#5a00aa", dropdown_fg_color="#4a4a4a",
                                                    height=40, dropdown_font=font_conf, fg_color="#343638")
        self.filter_option_menu.grid(row=row, column=1, columnspan=2, padx=10, pady=(2, 10))
        self.filter_option_menu.configure(font=font_conf)
        self.filter_option_menu.set("-No Filter-")
        row += 1

        # apply filter Button
        self.apply_filter_btn = ctk.CTkButton(self, text="Apply The Filter", fg_color="#042d64",
                                              corner_radius=10, border_spacing=1,
                                              border_color="#3a596d", border_width=1, height=35,
                                              command=self.apply_filter_)

        self.apply_filter_btn.grid(row=row, column=1, columnspan=self.kernel_size, padx=10, pady=(5, 0))
        self.apply_filter_btn.configure(font=ctk.CTkFont(family=FONTS['Montserrat'], weight="bold", size=BTN_FS))

        row += 1

        # progressbar
        self.progressbar = self.create_progressbar(col=1, row=row)
        self.progressbar_row = row
        row += 1

        # padding label
        self.label_padding = CTkLabel(self, text="Padding:", justify="left")
        self.label_padding.grid(row=row, column=1, padx=(5, 0), columnspan=2, pady=(1, 5),
                                sticky="w")
        self.label_padding.configure(font=font_conf)
        # Padding entry
        self.padding_entry = CTkEntry(self, width=40)
        self.padding_entry.grid(row=row, column=2, columnspan=2, padx=5, sticky="ew")
        self.padding_entry.insert(0, "0")
        row += 1

        # Stride label
        self.label_Stride = CTkLabel(self, text="Stride:", justify="left")
        self.label_Stride.grid(row=row, column=1, padx=(5, 0), columnspan=2, pady=(1, 5),
                               sticky="w")
        self.label_Stride.configure(font=font_conf)
        # Stride entry
        self.stride_entry = CTkEntry(self, width=40)
        self.stride_entry.grid(row=row, column=2, columnspan=2, padx=5, sticky="ew")
        self.stride_entry.insert(0, "1")
        row += 1

        # args label
        self.label_args = CTkLabel(self, text="arguments :", justify="left")
        self.label_args.grid(row=row, column=1, padx=(5, 0), columnspan=self.kernel_size, pady=(1, 5), sticky="w")
        self.label_args.configure(font=font_conf)
        row += 1
        # Additional arguments entry
        self.args_textbox = CTkTextbox(self, height=10, wrap="word", border_spacing=25, font=font_conf)
        self.args_textbox.grid(row=row, sticky="news", column=1, columnspan=self.kernel_size, padx=1,
                               pady=(0, 10))
        self.args_textbox_placeholder = "use this format:\narg1=value1\narg2=value2\narg3=value3\n...."
        self.args_textbox.insert("0.0", self.args_textbox_placeholder)
        self.args_textbox.bind("<FocusIn>", self.clear_placeholder)

        # Make the last row expandable
        self.rowconfigure(row, weight=1)

    def create_progressbar(self, col, row):
        progressbar = ctk.CTkProgressBar(self, mode="indeterminate", height=5,
                                         fg_color="#f1f1f1", progress_color="#f1f1f1")
        progressbar.grid(row=row, column=col, columnspan=int(self.kernel_size) - 1, padx=1, sticky='ew', pady=(10, 10))
        return progressbar

    def clear_placeholder(self, event):
        print("clear_placeholder event", event)
        if self.args_textbox.get("0.0", "end-1c") == self.args_textbox_placeholder:
            self.args_textbox.delete("0.0", "end")

    def apply_filter_(self):
        import threading

        def apply_filter_threaded(filter_):
            self.progressbar.configure(fg_color="#121e4c")
            self.progressbar.start()
            filter_dir = self.filters[filter_]
            args_srt = self.args_textbox.get("1.0", "end-1c")
            args = ["--padding", int(self.padding_entry.get()),
                    "--stride", int(self.stride_entry.get()),
                    "--kernel_size", int(self.kernel_size)
                    ]

            if not args_srt.startswith("use this format:"):
                for arg_str in args_srt.split("\n"):
                    parts = arg_str.split("=")
                    if len(parts) >= 2 and all(part.strip() for part in parts[:2]):
                        k, v = parts[:2]
                        args.extend([f"--{k.strip()}", str(v.strip())])

            self.parent.apply_filter(filter_dir, filter_, *args)
            print(self.name_id, "filter is ", filter_dir, filter_)

            self.progressbar.stop()
            # progressbar
            progressbar = self.create_progressbar(row=self.progressbar_row, col=1)
            self.progressbar.destroy()
            self.progressbar = progressbar

        def start_progressbar():
            self.progressbar.start()

        filter_name = self.filter_option_menu.get()
        if filter_name != "-No Filter-":
            t1 = threading.Thread(target=apply_filter_threaded, args=(filter_name,))
            t2 = threading.Thread(target=start_progressbar)

            # Start threads
            t1.start()
            t2.start()

    def get_filters(self) -> dict:
        import os
        import string

        def get_python_files(directory) -> dict:
            python_files = {}
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        file = file.rstrip("py")
                        text = str(file).translate(
                                str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
                        formatted_text = ' \n'.join(text[i:i + 15] for i in range(0, 31, 15))
                        python_files[formatted_text.strip().title()] = os.path.abspath(file_path)
            return python_files

        filters_dir = "filter_script"
        os.makedirs(filters_dir, exist_ok=True)

        filters = get_python_files(filters_dir)
        filters["Gray Scale Filter"] = os.path.abspath('gray_scale.py')
        print(self.name_id, "found filters:", filters, sep="\n")
        return filters

    def set_kernel_size(self, size):
        self.kernel_size = size
        print("kernel_size is ", self.kernel_size)
