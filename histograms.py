import matplotlib
import numpy as np
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
from PIL import Image

matplotlib.use('TkAgg')


class ImageHistogramPlot:
    def __init__(self, image_path):

        self.image_path = image_path
        self._figure = self.create_plot()

    def create_plot(self):
        # Load the image
        image = Image.open(self.image_path)
        image_array = np.array(image)

        # Check if the image is grayscale
        if len(image_array.shape) == 2:
            is_grayscale = True
        else:
            is_grayscale = False

        if not is_grayscale:
            figure = Figure(figsize=(10, 8), dpi=100)
            axes = figure.subplots(nrows=2, ncols=2)
            figure.tight_layout(pad=6.5)
            num_bins = 256
            # Plot the grayscale histogram
            axes[0, 0].hist(image_array.flatten(), bins=num_bins, color='black')
            axes[0, 0].set_title('Grayscale')
            # Plot histograms for each color channel
            for i, color in enumerate(['red', 'green', 'blue']):
                y = image_array[:, :, i].flatten()
                hist = np.histogram(y, bins=num_bins + 1)[0]
                x = np.arange(0, num_bins + 1)
                axes[(i + 1) // 2, (i + 1) % 2].bar(x, hist, color=color, alpha=0.7)
                axes[(i + 1) // 2, (i + 1) % 2].set_title(color.capitalize() + ' Channel')
        else:
            figure = Figure(figsize=(6, 4), dpi=100)
            axes = figure.add_subplot(1, 1, 1)
            # Plot the histogram of the entire image
            axes.hist(image_array.flatten(), bins=256, color='gray')
            axes.set_title('Histogram of the Grayscale Image')
            axes.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

        return figure

    def fig2img(self, width, height):
        from PIL import Image, ImageTk
        from io import BytesIO
        self._figure.set_size_inches((width / 100, height / 100))
        figure = self._figure
        # Step 1: Render the figure to a matplotlib canvas
        buffer = BytesIO()
        figure.savefig(buffer, format='png', dpi=100)
        buffer.seek(0)

        # Step 2: Convert the PNG buffer to a PIL Image
        image = Image.open(buffer).convert('RGB')
        image = image.resize((width, height))  # Resize if necessary

        # Step 3: Convert the PIL Image to a PIL ImageTk PhotoImage
        photo_image = ImageTk.PhotoImage(image)

        return photo_image
