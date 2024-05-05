import os

import matplotlib.pyplot as plt
import numpy as np

import get_args


# Function to perform contra-harmonic mean filtering
def contra_harmonic_mean_filter(image, filter_size, q=1):
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
            # Apply contra harmonic mean operation
            numerator = np.sum(neighborhood ** (q + 1))
            denominator = np.sum(neighborhood ** q)
            filtered_image[i, j] = numerator / (denominator + 1e-6) if denominator != 0 else 0

    return filtered_image


def main():
    args = get_args.aget()
    image = plt.imread(args.img_path)
    try:
        q = float(args.Q)
    except (TypeError, NameError):
        q = 1

    new_img = contra_harmonic_mean_filter(image, filter_size=int(args.kernel_size), q=q)
    out = "temp.jpg"
    plt.imsave(out, new_img)
    print(out, end='')


if __name__ == "__main__":
    main()
