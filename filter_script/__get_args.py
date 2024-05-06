import argparse


def aget():
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path", help="img path")
    parser.add_argument("--padding", type=int, help="padding")
    parser.add_argument("--stride", type=int, help="stride")
    parser.add_argument("--kernel_size", help="kernel_size")
    parser.add_argument("--Q", help="for contra_harmonic_mean_filter")
    return parser.parse_args()
