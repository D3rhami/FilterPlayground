import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import generic_filter

import get_args


def geometric_mean_filter(image, filter_size):
    # Define the geometric mean function
    def geometric_mean(values):
        return np.prod(values) ** (1.0 / len(values))

    # Apply the geometric mean filter using generic_filter
    filtered_image = generic_filter(image, geometric_mean, size=filter_size)

    return filtered_image


def main():
    args = get_args.aget()
    image = plt.imread(args.img_path)
    new_img = geometric_mean_filter(image, filter_size=int(args.kernel_size))
    out = "temp.jpg"
    plt.imsave(out, new_img)
    print(out, end='')


if __name__ == "__main__":
    main()
