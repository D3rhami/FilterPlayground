import cv2

from FilterPlayground.filter_script import __get_args


def gray_scale(img_path, ):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    return img


def main():
    args = __get_args.aget()
    new_img = gray_scale(args.img_path, )
    out = "temp.jpg"
    cv2.imwrite(out, new_img)
    print(out, end='')


if __name__ == "__main__":
    main()
