import os
from tkinter import messagebox

import customtkinter as ctk

from assets import BTN_FS, FONTS, PIC_DIR


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, width=50, **kwargs):
        super().__init__(master, width=width, corner_radius=0, **kwargs)
        self.name_id = "slider class"
        self.parent = master
        self.width = width
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        row = 0
        font_conf1 = ctk.CTkFont(family=FONTS['Montserrat'], weight="bold", size=BTN_FS)

        # ttk.Separator(self, orient='horizontal').pac k(fill='x', pad y=5)
        # progressbar

        # Open Image Button
        self.open_image_btn = ctk.CTkButton(self, text="Open Image", fg_color="#042d64",
                                            command=self.open_image_event,
                                            border_color="#3a596d", border_width=1,
                                            height=35, width=140)
        self.open_image_btn.grid(row=row, column=1, padx=10, pady=10)
        self.open_image_btn.configure(font=font_conf1)
        row += 1

        # Swap Images Button
        self.sawp_images_btn = ctk.CTkButton(self, text="Sawp Images", fg_color="#042d64",
                                             command=self.swap_images,
                                             border_color="#3a596d", border_width=1,
                                             height=35, width=140)
        self.sawp_images_btn.grid(row=row, column=1, padx=10, pady=(25, 10))
        self.sawp_images_btn.configure(font=font_conf1)
        row += 1
        # Add New Function Button
        self.add_function_btn = ctk.CTkButton(self, text="Add New\nFunction", command=self.add_function_event,
                                              border_color="#3a596d", border_width=1,
                                              fg_color="#042d64", height=50, width=140)
        self.add_function_btn.grid(row=row, column=1, padx=10, pady=10)
        self.add_function_btn.configure(font=font_conf1)
        row += 1

        # Save Image Button
        self.save_image_btn = ctk.CTkButton(self, text="Save Image", command=self.save_image_event,
                                            border_color="#3a596d", border_width=1,
                                            height=35, width=140, fg_color="#042d64")
        self.save_image_btn.grid(row=row, column=1, padx=10, pady=10)
        self.save_image_btn.configure(font=font_conf1)
        row += 1

        self.progressbar = self.create_progressbar(col=1, row=row, pad_y=(5, 5), column_span=1)
        self.progressbar_row = row
        row += 1

        # axis toggle
        self.axis_toggle_box = ctk.CTkCheckBox(master=self, text="axis on".title(), fg_color="#042d64",
                                               hover_color="gray", font=font_conf1, command=self.axis_toggle)
        self.axis_toggle_box.grid(row=row, column=1, padx=10, pady=(10, 5))
        row += 1
        # histogram toggle
        self.hist_toggle_box = ctk.CTkCheckBox(master=self, text="Histogram".title(), fg_color="#042d64",
                                               hover_color="gray", font=font_conf1, command=self.histogram_toggle)
        self.hist_toggle_box.grid(row=row, column=1, padx=10, pady=(5, 10))
        row += 1

        # ----------
        font_conf2 = ctk.CTkFont(family=FONTS['Montserrat'], size=BTN_FS)
        # appearance_mode_label
        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:", anchor="w",
                                                  font=ctk.CTkFont(size=BTN_FS, weight="bold"))
        self.appearance_mode_label.grid(row=row, column=1, pady=(10, 0))
        row += 1

        self.appearance_mode_option_menu = ctk.CTkOptionMenu(self, fg_color="gray", button_color="#140180",
                                                             values=["System", "Dark", "Light"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=row, column=1, padx=10, pady=(0, 5))
        self.appearance_mode_option_menu.configure(font=font_conf2)
        row += 1

        # scaling_label
        self.scaling_label = ctk.CTkLabel(self, text="UI Scaling:", anchor="w",
                                          font=ctk.CTkFont(size=BTN_FS, weight="bold"))
        self.scaling_label.grid(row=row, column=1, pady=(10, 0))
        self.scaling_option_menu = ctk.CTkOptionMenu(self, values=[f"{r}%" for r in range(100, 251, 10)],
                                                     button_color="#140180",
                                                     command=self.change_scaling_event, fg_color="gray")
        row += 1

        self.scaling_option_menu.grid(row=row, column=1, padx=10, pady=(2, 20))
        self.scaling_option_menu.set("100%")
        self.scaling_option_menu.configure(font=font_conf2)
        row += 1

        # Exit Button
        self.exit_btn = ctk.CTkButton(self, text="Exit", command=self.exit_button_event,
                                      height=35, width=140)
        self.exit_btn.grid(row=row, column=1, padx=10, pady=(20, 10))
        self.exit_btn.configure(font=ctk.CTkFont(family=FONTS['Montserrat'], size=BTN_FS + 2), fg_color="#9d0000")

    def axis_toggle(self):

        import threading

        if self.axis_toggle_box.get() == 1 and self.hist_toggle_box.get() == 1:
            self.hist_toggle_box.deselect()

        def toggle():
            self.progressbar.configure(fg_color="#121e4c")
            self.progressbar.start()

            print("axis :", self.axis_toggle_box.get())
            self.parent.axis_toggle(self.axis_toggle_box.get())

            self.progressbar.stop()
            # progressbar
            progressbar = self.create_progressbar(row=self.progressbar_row, col=1, pad_y=(5, 5), column_span=1)
            self.progressbar.destroy()
            self.progressbar = progressbar

        def start_progressbar():
            self.progressbar.start()

        t1 = threading.Thread(target=toggle)
        t2 = threading.Thread(target=start_progressbar)

        # Start threads
        t1.start()
        t2.start()

        print(self.name_id, "apply convolution ended")

    def histogram_toggle(self):
        import threading

        if self.axis_toggle_box.get() == 1 and self.hist_toggle_box.get() == 1:
            self.axis_toggle_box.deselect()

        def toggle():
            self.progressbar.configure(fg_color="#121e4c")
            self.progressbar.start()

            self.parent.histogram_toggle(self.hist_toggle_box.get())

            self.progressbar.stop()
            # progressbar
            progressbar = self.create_progressbar(row=self.progressbar_row, col=1, pad_y=(5, 5), column_span=1)
            self.progressbar.destroy()
            self.progressbar = progressbar

        def start_progressbar():
            self.progressbar.start()

        t1 = threading.Thread(target=toggle)
        t2 = threading.Thread(target=start_progressbar)

        # Start threads
        t1.start()
        t2.start()

        print(self.name_id, "toggled histogram ended")

    def open_image_event(self):
        import tkinter.filedialog as filedialog

        def open_image_dialog():
            if not os.path.exists(PIC_DIR):
                os.makedirs(PIC_DIR)

            file_path = filedialog.askopenfilename(initialdir=PIC_DIR,
                                                   filetypes=[("Image files", "*.png;*.jpg;*.jpeg;")])
            return file_path

        img_path = open_image_dialog()
        if img_path is not None:
            self.parent.set_raw_img(img_path)
        print(self.name_id, "opened image")

    def add_function_event(self):
        def create_file(args_dict, function_name):
            if function_name == "":
                function_name = "new_function"

            # Create the filter_script directory if it doesn't exist
            script_dir = "./filter_script"
            if not os.path.exists(script_dir):
                os.makedirs(script_dir)

            file_path = os.path.join(script_dir, f"{function_name}.py")
            with open(os.path.abspath(file_path), "w") as f:
                f.write("# Generated file\n\n"
                        f"""
import matplotlib.pyplot as plt
import numpy as np
import get_args

def {function_name}(image, filter_size,{','.join([f'{k}={v}' for k, v in args_dict.items()]),}):
    pass
def main():
    args = get_args.aget()
    image = plt.imread(args.img_path)
    new_img = {function_name}(image, filter_size=int(args.kernel_size))#fix here as well
    out = "temp.jpg"
    plt.imsave(out, new_img)
    print(out, end='')
if __name__ == "__main__":
    main() """)
                for arg_name, arg_value in args_dict.items():
                    f.write(f"{arg_name} = {arg_value}\n")

            return file_path

        def create_popup():
            popup = ctk.CTkToplevel(self)
            popup.title("added new function")
            popup.geometry("350x500")
            popup.grab_set()
            font_conf = ctk.CTkFont(family=FONTS['Montserrat'], weight="bold", size=BTN_FS)

            ctk.CTkLabel(popup, text="Name of function", font=font_conf).grid(row=0, column=0, padx=10, pady=10)
            func_name = ctk.CTkEntry(popup)
            row = 0
            func_name.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            row += 1

            fixed = ctk.CTkLabel(popup, text="image, padding , stride is provided", font=font_conf)
            fixed.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky="w")
            row += 1

            ctk.CTkLabel(popup, text="Name input argument", font=font_conf).grid(row=row, column=0,
                                                                                 padx=10, pady=10)
            ctk.CTkLabel(popup, text="Default value", font=font_conf).grid(row=row, column=1, padx=10, pady=10)
            row += 1
            # Create entries for each row
            entries = []
            for _ in range(7):
                name_entry = ctk.CTkEntry(popup)
                name_entry.grid(row=row, column=0, padx=10, pady=5, sticky="e")

                value_entry = ctk.CTkEntry(popup)
                value_entry.grid(row=row, column=1, padx=10, pady=5)
                row += 1
                entries.append((name_entry, value_entry))

            # Create the "Add function and open code file" button
            def add_function_and_open_file():
                args_dict = {entry.get(): v.get() for entry, v in entries if entry.get() and v.get()}
                file_path = create_file(args_dict, func_name.get())
                os.startfile(file_path)
                popup.destroy()

            add_function_btn = ctk.CTkButton(popup, text="Add function and open code file", font=font_conf,
                                             fg_color="#042d64", command=add_function_and_open_file)
            add_function_btn.grid(row=row, column=0, columnspan=2, padx=10, pady=10)

        try:
            create_popup()
            print(self.name_id, "added new function")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred in added new function:\n {str(e)}")
            print("Error", f"An error occurred in added new function:\n {str(e)}")

    def save_image_event(self):
        # Logic to call master function "save_new_image"
        self.parent.save_new_image()
        print(self.name_id, "saved image")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        print(self.name_id, "changed appearance_mode")

    def change_scaling_event(self, new_scaling: str):
        self.parent.change_scale(new_scaling)

    def exit_button_event(self):
        self.parent.confirm_exit()

    def create_progressbar(self, col, row, pad_y, column_span):
        progressbar = ctk.CTkProgressBar(self, mode="indeterminate", height=5, width=self.width - 6,
                                         fg_color="#f1f1f1", progress_color="#f1f1f1")
        progressbar.grid(row=row, column=col, columnspan=column_span, padx=1, pady=pad_y)
        return progressbar

    def swap_images(self):
        self.parent.swap_images()
