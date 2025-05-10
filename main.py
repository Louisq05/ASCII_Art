"""
@inspo: Viet Nguyen <nhviet1009@gmail.com>
@author: Louis Quibeuf <louisquibeufworkspace@gmail.com>
"""
import argparse  # Allow command line arguments like --input image.jpg
import cv2  # To open and read images
import numpy as np  # For matrix calculations and pixel averaging


def get_args():  # Definition of CLI arguments
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input", type=str, default="data/input.jpg", help="Path to input image")  # Entry path
    parser.add_argument("--output", type=str, default="data/output.txt", help="Path to output text file")  # Output path
    parser.add_argument("--mode", type=str, default="complex", choices=["simple", "complex"], 
                        help="10 or 70 different characters")  # Complexity of the ASCII charset
    parser.add_argument("--num_cols", type=int, default=150, help="Number of characters for output width")  # Width in characters
    args = parser.parse_args()
    return args


def main(opt):
    if opt.mode == "simple":
        CHAR_LIST = '@%#*+=-:. '  # Basic character set (low detail)
    else:
        CHAR_LIST = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "  # Detailed character set
    num_chars = len(CHAR_LIST)
    num_cols = opt.num_cols
    image = cv2.imread(opt.input)  # Load image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
    height, width = image.shape  # Get image dimensions
    cell_width = width / opt.num_cols  # Width of one ASCII "pixel"
    cell_height = 2 * cell_width  # Height of one ASCII "pixel" (adjusted for character proportions)
    num_rows = int(height / cell_height)  # Calculate number of rows in output

    if num_cols > width or num_rows > height:  # Fallback if resolution is too high
        print("Too many columns or rows. Use default setting")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)

    output_file = open(opt.output, 'w')  # Open output file
    for i in range(num_rows):  # Loop through each row of cells
        for j in range(num_cols):  # Loop through each column of cells
            # Crop cell region, compute its mean grayscale value, and map it to an ASCII character
            output_file.write(
                CHAR_LIST[min(int(np.mean(image[int(i * cell_height):min(int((i + 1) * cell_height), height),
                                          int(j * cell_width):min(int((j + 1) * cell_width),
                                                                  width)]) * num_chars / 255), num_chars - 1)])
        output_file.write("\n")  # Newline at end of row
    output_file.close()  # Close and save file

def interactive_inputs():
    print("Welcome to the ASCII generator app !\n")
    input_path = input("[default: data/input.jpg]\nPlease enter the path to your input image : ") or "data/input.jpg"
    output_path = input("[default: data/output.jpg]\nPlease enter the path to your input image : ") or "data/output.jpg"

    mode = ""
    while mode not in ["simple","complex"] :
        mode = input("[default: complex]\nChoose a caracter complexity (simple/complex) : ") or "complex"

        try:
            num_cols = int(input("[default: 150]\nNumber of characters for whidth : ") or 150)
        except ValueError:
            num_cols = 150

        return argparse.Namespace(input=input_path, output=output_path, mode=mode, num_cols=num_cols)

if __name__ == '__main__':
    choice = input("Would you like to use the interactive? (y/n) : ").lower()
    if choice == 'y' :
        opt = interactive_inputs()
    else :
        opt = get_args()
    main(opt)


"""
Example of instruction :
python main.py --input data/input.jpg --output data/output.txt --mode complex --num_cols 150
"""
