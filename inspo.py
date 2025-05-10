"""
@author: Viet Nguyen <nhviet1009@gmail.com>
"""
import argparse # Allow comand like --input image.jpg
import cv2 # To open and read images
import numpy as np # For matrix calculation and pixel average


def get_args(): # Definition of CLI arguments
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input", type=str, default="data/input.jpg", help="Path to input image") # entry path
    parser.add_argument("--output", type=str, default="data/output.txt", help="Path to output text file") # output path
    parser.add_argument("--mode", type=str, default="complex", choices=["simple", "complex"], 
                        help="10 or 70 different characters") # complexity of the characters
    parser.add_argument("--num_cols", type=int, default=150, help="number of character for output's width") # Number of ascii columns
    args = parser.parse_args()
    return args


def main(opt):
    if opt.mode == "simple":
        CHAR_LIST = '@%#*+=-:. '
    else:
        CHAR_LIST = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    num_chars = len(CHAR_LIST)
    num_cols = opt.num_cols
    image = cv2.imread(opt.input) # Image reading
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # translation to grey levels
    height, width = image.shape # ascii matrix definition
    cell_width = width / opt.num_cols # Width
    cell_height = 2 * cell_width # Height
    num_rows = int(height / cell_height)
    if num_cols > width or num_rows > height: # Adaptation of the column number
        print("Too many columns or rows. Use default setting")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)

    output_file = open(opt.output, 'w')
    for i in range(num_rows):# Building of the ascii art
        for j in range(num_cols):
            output_file.write(
                CHAR_LIST[min(int(np.mean(image[int(i * cell_height):min(int((i + 1) * cell_height), height),
                                          int(j * cell_width):min(int((j + 1) * cell_width),
                                                                  width)]) * num_chars / 255), num_chars - 1)])
        output_file.write("\n")
    output_file.close() # Saving of the art


if __name__ == '__main__':
    opt = get_args()
    main(opt)