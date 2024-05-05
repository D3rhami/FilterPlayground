import matplotlib.pyplot as plt
import numpy as np

import get_args


# Function to perform harmonic mean filtering
def harmonic_mean_filter(image, filter_size):
    # Calculate half of the size
    add_size = filter_size // 2

    # Apply padding to the image
    padded_image = np.pad(image, ((add_size, add_size), (add_size, add_size), (0, 0)), mode='constant')
    filtered_image = np.zeros_like(image)

    # Iterate over image pixels
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # Extract the neighborhood
            neighborhood = padded_image[i:i + filter_size, j:j + filter_size]
            # Apply harmonic mean operation
            # Handle division by zero by adding a small value (epsilon)
            filtered_image[i, j] = filter_size ** 2 / np.sum(1 / (neighborhood + 1e-6), axis=(0, 1))

    return filtered_image


def main():
    args = get_args.aget()
    image = plt.imread(args.img_path)
    new_img = harmonic_mean_filter(image, filter_size=int(args.kernel_size))
    out = "temp.jpg"
    plt.imsave(out, new_img)
    print(out, end='')

if __name__ == "__main__":
    main()
