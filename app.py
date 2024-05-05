import datetime
import os
import tkinter.messagebox as messagebox

import customtkinter as ctk
from PIL import Image

from assets import FONT_SIZE, FONTS, PADDING_APP, PIC_DIR
from filterConfigurator import FilterConfigurator, KernelConfigurator
from sidebar import Sidebar

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.raw_img_path = os.path.abspath("placeHolder.jpg")
        self.mod_img_path = os.path.abspath("placeHolder.jpg")
        self.temp_out = "temp.jpg"
        self.name_id = "app main"
        self.title("FilterPlayground by AmirHoseein Derhami")
        self.iconbitmap("logo.ico")
        sidebar_width = 140
        self.middel_width = 180
        self.height = 600
        self.width = sidebar_width + self.middel_width + self.height * 2
        self.geometry(f"{self.width + PADDING_APP[0]}x{self.height + PADDING_APP[1]}")
        self.protocol("WM_DELETE_WINDOW", self.confirm_exit)  # Handle window closing event
        self.resizable(True, False)

        # create sidebar
        self.sidebar = Sidebar(self, width=sidebar_width)
        self.sidebar.grid(row=1, column=1, rowspan=2)
        self.grid_rowconfigure(1, weight=1)

        font_config = ctk.CTkFont(family=FONTS['Montserrat'], weight="bold", size=int(FONT_SIZE * .9))
        # create labels for raw image and modified image
        self.raw_img_label = ctk.CTkLabel(self, text="Raw Image", justify="center")
        self.raw_img_label.grid(row=1, column=2, sticky="ew", )
        self.raw_img_label.configure(font=font_config)

        self.mod_img_label = ctk.CTkLabel(self, text="Modified image", justify="center")
        self.mod_img_label.grid(row=1, column=4, sticky="ew", )
        self.mod_img_label.configure(font=font_config)

        # create tabview
        self.tabview = ctk.CTkTabview(self, width=self.middel_width,
                                      text_color="black", height=30,
                                      segmented_button_selected_color="#ffaec8",
                                      segmented_button_selected_hover_color="#c81e50"
                                      )
        self.tabview.grid(row=1, column=3, rowspan=2, padx=1, pady=5, sticky="ns")
        self.tabview.segmented_button.configure(font=font_config)

        self.tabview.add("Conv")
        self.tabview.add("Filters")
        tab_conv = self.tabview.tab("Conv")
        tab_filters = self.tabview.tab("Filters")

        self.kernel_conf = KernelConfigurator(master=self, frame_root=tab_conv)
        self.kernel_conf.pack()

        self.filter_conf = FilterConfigurator(master=self, frame_root=tab_filters)
        self.filter_conf.pack()

        # configure grid weights and column widths
        self.grid_columnconfigure(1, weight=0, minsize=sidebar_width)
        self.grid_columnconfigure(2, weight=1, minsize=self.height)
        self.grid_columnconfigure(3, weight=0, minsize=self.middel_width)
        self.grid_columnconfigure(4, weight=1, minsize=self.height)
        self.grid_rowconfigure(1, weight=1)

        # load and display images
        self.raw_img = self.load_and_resize_image(self.raw_img_path, size=self.height)
        self.mod_img = self.load_and_resize_image(self.mod_img_path, size=self.height)

        self.raw_img_canvas = self.create_img_in_canvas(row=2, col=2, img=self.raw_img)
        self.mod_img_canvas = self.create_img_in_canvas(row=2, col=4, img=self.mod_img)

        # set label top rows
        self.update_top_labels()

    def load_and_resize_image(self, image_path, size):
        from PIL import Image, ImageOps, ImageTk

        image = Image.open(image_path)
        image = ImageOps.pad(image, (size, size), Image.Resampling.LANCZOS)
        print(self.name_id, "resized image", image_path)
        return ImageTk.PhotoImage(image)

    def confirm_exit(self):
        # if messagebox.askyesno("Confirmation", 'Are you sure you want to exit?'):
        print("exit ...")
        self.destroy()

    def axis_toggle(self, axis):
        import matplotlib.pyplot as plt
        if axis:
            # Plot your image with axis
            def plot(img_path, out_dir):
                plt.imshow(plt.imread(img_path), cmap='gray')
                plt.axis('on')
                fig = plt.gcf()
                plt.gca().set_aspect('equal', adjustable='box')  # Make the aspect ratio equal
                plt.gcf().set_size_inches(self.height / fig.dpi, self.height / fig.dpi)
                plt.savefig(out_dir, bbox_inches='tight')

            plot(self.raw_img_path, "axis_on_raw.jpg")
            plot(self.mod_img_path, "axis_on_mod.jpg")

            # load and display images
            self.raw_img = self.load_and_resize_image("axis_on_raw.jpg", size=self.height)
            self.mod_img = self.load_and_resize_image("axis_on_mod.jpg", size=self.height)

            self.raw_img_canvas = self.create_img_in_canvas(row=2, col=2, img=self.raw_img)
            self.mod_img_canvas = self.create_img_in_canvas(row=2, col=4, img=self.mod_img)

        else:
            # load and display images
            self.mod_img = self.load_and_resize_image(self.mod_img_path, size=self.height)
            self.raw_img = self.load_and_resize_image(self.raw_img_path, size=self.height)

            self.mod_img_canvas = self.create_img_in_canvas(row=2, col=4, img=self.mod_img)
            self.raw_img_canvas = self.create_img_in_canvas(row=2, col=2, img=self.raw_img)

        print("axis toggled")

    def histogram_toggle(self, mode):
        if mode:
            from histograms import ImageHistogramPlot

            # load and display images
            self.raw_img = ImageHistogramPlot(self.raw_img_path).fig2img(self.height, self.height)
            self.mod_img = ImageHistogramPlot(self.mod_img_path).fig2img(self.height, self.height)

            self.raw_img_canvas = self.create_img_in_canvas(row=2, col=2, img=self.raw_img)
            self.mod_img_canvas = self.create_img_in_canvas(row=2, col=4, img=self.mod_img)

        else:
            # load and display images
            self.raw_img = self.load_and_resize_image(self.raw_img_path, size=self.height)
            self.mod_img = self.load_and_resize_image(self.mod_img_path, size=self.height)

            self.raw_img_canvas = self.create_img_in_canvas(row=2, col=2, img=self.raw_img)
            self.mod_img_canvas = self.create_img_in_canvas(row=2, col=4, img=self.mod_img)

        print("histogram toggled")

    def change_scale(self, new_scaling: str):
        print("old height:", self.height, "old width", self.width)

        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
        self.width = int((self.width - 40) * new_scaling_float)
        self.height = int((self.height - 40) * new_scaling_float)
        print("new height:", self.height, "new width", self.width)
        self.geometry(f"{self.width + PADDING_APP[0]}x{self.height + PADDING_APP[1]}")

        # Reload and resize the images
        self.raw_img = self.load_and_resize_image(self.raw_img_path, size=self.height)
        self.mod_img = self.load_and_resize_image(self.mod_img_path, size=self.height)

        # fix label
        self.raw_img_label.configure(text=f"Raw image in [{('-' * 1000)[:100]}]")

        # Update the images on the canvas
        self.raw_img_canvas.destroy()
        self.create_img_in_canvas(row=2, col=2, img=self.raw_img)

        self.mod_img_canvas.destroy()
        self.create_img_in_canvas(row=2, col=4, img=self.mod_img)

        self.update_top_labels()
        print(self.name_id, "scale", new_scaling_float)

    def update_top_labels(self):
        import cv2

        def get_image_shape(image_path):
            image = cv2.imread(image_path)
            if image is not None:
                height, width, channels = image.shape
                return f"{height}x{width}x{channels}"
            else:
                print("Error: Unable to read the image.")
                return "-x-"

        extension = os.path.splitext(self.raw_img_path)[1]
        shape = get_image_shape(self.raw_img_path)
        raw_name = os.path.splitext(self.raw_img_path)[0][:40]
        if len(self.raw_img_path) > 42:
            raw_name += "..."

        self.raw_img_label.configure(text=f"Raw image in [{raw_name}{extension}] {shape}")
        shape = get_image_shape(self.mod_img_path)
        self.mod_img_label.configure(text=f"Modified image {shape}")

    def create_img_in_canvas(self, col, img, row):
        canvas = ctk.CTkCanvas(self, width=self.height, height=self.height)
        center = self.height // 2
        canvas.create_image(center, center, image=img)
        canvas.grid(row=row, column=col, padx=5, pady=(0, 5))
        return canvas

    def set_raw_img(self, img_path):
        self.raw_img_path = img_path
        self.mod_img_path = img_path
        # Reload and resize the images
        self.raw_img = self.load_and_resize_image(image_path=img_path, size=self.height, )
        self.raw_img_canvas.destroy()
        self.create_img_in_canvas(row=2, col=2, img=self.raw_img)
        # Reload and resize the images
        self.mod_img = self.load_and_resize_image(image_path=img_path, size=self.height, )
        self.mod_img_canvas.destroy()
        self.create_img_in_canvas(row=2, col=4, img=self.raw_img)
        self.update_top_labels()

        print(self.name_id, "src image path:", img_path)

    def save_new_image(self):
        import tkinter.filedialog as filedialog

        if not os.path.exists(PIC_DIR):
            os.makedirs(PIC_DIR)
        timestamp = datetime.datetime.now().strftime("%d.%m.%Y_%H.%M")
        file_name = f"mod_image_{timestamp}.jpg"
        file_path = filedialog.asksaveasfilename(initialdir=PIC_DIR,
                                                 initialfile=file_name,
                                                 filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")],
                                                 defaultextension="JPEG")
        if file_path:
            try:
                # Load the image from the path
                image = Image.open(self.mod_img_path)
                image.save(file_path)  # Save the image object
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        print(self.name_id, "saved image in:", file_path)

    def apply_filter(self, filter_dir, filter_name, *args):
        try:
            import subprocess
            import inspect
            import importlib.util
            import sys
            import cv2

            def run_python_script(file_path_, args_):
                command = [sys.executable, file_path_] + args_
                try:
                    result = subprocess.run(command, capture_output=True, text=True, check=True)
                    return result.stdout
                except subprocess.CalledProcessError as es:
                    return f"Error: {es.stderr}"

            os.remove(self.temp_out) if os.path.exists(self.temp_out) else None
            args = ["--img_path", f"{self.raw_img_path}"] + [str(a) for a in args]
            print("$ args:", args)
            output = run_python_script(filter_dir, args).strip()

            print("Script Output:", str(output))
            if output is not None:
                # Reload and resize the images
                self.mod_img_path=self.temp_out
                self.mod_img = self.load_and_resize_image(image_path=output, size=self.height, )
                self.mod_img_canvas.destroy()
                self.create_img_in_canvas(row=2, col=4, img=self.mod_img)
                self.update_top_labels()

                print(self.name_id, "@ filter is ", filter_dir, filter_name, "args:", args)

            else:
                messagebox.showerror("Error", "An error occurred in output of filter")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred in applying the filter:\n {str(e)}")
            print("Error", f"An error occurred in applying the filter:\n {str(e)}")

    def apply_convolution(self, kernel, padding, stride):
        import matplotlib.pyplot as plt
        import numpy as np
        from scipy.signal import convolve2d

        try:
            image = plt.imread(self.raw_img_path)

            # Function to convert the image to grayscale
            def rgb2gray(rgb):
                return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])

            image = np.pad(image, padding, mode='constant')
            image = rgb2gray(image)
            print("padding :", padding, "stride: ", stride)
            print("kernel:", kernel, kernel.shape)
            print("image:", image.shape)
            # Apply convolution with the emboss filter
            filtered_image = convolve2d(image, kernel, mode='same')[::stride, ::stride]
            # Clip the pixel values to ensure they are within the valid range [0, 255]
            filtered_image = np.clip(filtered_image, 0, 255)
            print("@@ half done apply convolution")
            plt.imsave(self.temp_out, filtered_image, cmap='gray')

            # Reload and resize the images
            self.mod_img_path = self.temp_out
            self.mod_img = self.load_and_resize_image(image_path=self.temp_out, size=self.height, )
            self.mod_img_canvas.destroy()
            self.create_img_in_canvas(row=2, col=4, img=self.mod_img)
            self.update_top_labels()

            print(self.name_id, "@@ convolution is ", kernel, filtered_image)
        except Exception as err:
            messagebox.showerror("Error", f"An error occurred in applying the convolution:\n {str(err)}")
            print("Error", f"An error occurred in applying the convolution:\n {str(err)}")


def create_app():
    print("new app create in ", datetime.datetime.now(), )
    app = App()
    app.mainloop()


if __name__ == "__main__":
    create_app()
