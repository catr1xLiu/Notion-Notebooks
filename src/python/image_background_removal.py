# A simple utility that turns pure-black background images into transparent background images.
#
# This makes mathematical illustrations in notebooks look much better.
# 
# Example usage: python .\src\image_background_removal.py "C:\Users\caTr1x\Pictures\

import os
import sys
from PIL import Image

def remove_black_background(image_path, output_path):
    """
    Opens a PNG image, makes black pixels transparent, and saves the result.

    Args:
        image_path (str): The full path to the input PNG image.
        output_path (str): The full path where the output image will be saved.
    """
    try:
        # Open the image
        img = Image.open(image_path)

        # Ensure the image is in RGBA format to handle transparency
        img = img.convert("RGBA")

        # Get the image data as a sequence of pixels
        datas = img.getdata()

        newData = []
        # Iterate through each pixel
        for item in datas:
            # Check if the pixel is black (R+G+B)*A < 5%
            if (item[0] + item[1] + item[2]) * item[3] < 0.05 * 255 * 3:
                # Replace it with a fully transparent pixel
                newData.append((0, 0, 0, 0))
            else:
                # Keep the original pixel
                newData.append(item)

        # Apply the new pixel data to the image
        img.putdata(newData)

        # Save the modified image
        img.save(output_path, "PNG")
        print(f"Successfully processed: {image_path}")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")


def main():
    """
    Main function to find and process all PNG files in a directory.
    """
    # Check if a directory path is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python3 image_background_removal.py <directory_path>")
        sys.exit(1)

    input_dir = sys.argv[1]

    # Check if the provided path is a valid directory
    if not os.path.isdir(input_dir):
        print(f"Error: The path '{input_dir}' is not a valid directory.")
        sys.exit(1)

    # Define the output directory path
    output_dir = os.path.join(input_dir, "result")

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Results will be saved in: {output_dir}")

    # Walk through the input directory
    for filename in os.listdir(input_dir):
        # Check if the file is a PNG image
        if filename.lower().endswith(".png"):
            image_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            remove_black_background(image_path, output_path)

if __name__ == "__main__":
    main()