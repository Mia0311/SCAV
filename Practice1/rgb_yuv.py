import sys
import subprocess
import numpy as np
from PIL import Image # need to install Pillow first
from scipy.fftpack import dct

# Task 1
def rgb_to_yuv(r, g, b):
    y = 0.257 * r + 0.504 * g + 0.098 * b + 16
    u = -0.148 * r - 0.291 * g + 0.439 * b + 128
    v = 0.439 * r - 0.368 * g - 0.071 * b + 128
    return y, u, v
# formula from theory slides
def yuv_to_rgb(y, u, v):
    b = 1.164 * (y - 16) + 2.018 * (u - 128)
    g = 1.164 * (y - 16) - 0.813 * (v - 128) - 0.391 * (u - 128)
    r = 1.164 * (y - 16) + 1.596 * (v - 128)
    return r, g, b

# Task 2
def resize_image(input_image, resized_image, width, height, quality):
    """
    Resize an image using FFmpeg.

    :param input_image: Input image file path
    :param resized_image: Output image file path
    :param width: New width for the resized image
    :param height: New height for the resized image
    :param quality: Output image quality
    """

    # ffmpeg -i p1_input1.jpeg -vf "scale=200:300" -q:v 10 -y p1_resized1.jpeg
    cmd = [
        "ffmpeg",
        "-i", input_image,
        "-vf", f"scale={width}:{height}",
        "-q:v", str(quality),
        "-y",  # Overwrite output file if it exists
        resized_image
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Resized image saved to {resized_image}")
    except subprocess.CalledProcessError as e:
        print(f"Error while resizing image: {e}")

# Task 3
def serpentine(input_image):
    try:
        img = Image.open(input_image)
        img = np.array(img)

        linear_sequence = []

        for i in range(8):
            if i % 2 == 0:
                for j in range(i, -1, -1):
                    linear_sequence.append(img[j][i - j])
            else:
                for j in range(0, i + 1):
                    linear_sequence.append(img[i - j][j])

        for i in range(1, 8):
            if i % 2 == 0:
                for j in range(7, i, -1):
                    linear_sequence.append(img[j][i + 7 - j])
            else:
                for j in range(i, 8):
                    linear_sequence.append(img[i + 7 - j][j])

        return linear_sequence
    except FileNotFoundError:
        print(f"File not found: {input_image}")
    except Exception as e:
        print(f"Error while processing the image: {e}")



# Task 4
def bw(input_image, bw_image, compression):
    """
    Resize an image using FFmpeg.

    :param input_image: Input image file path
    :param bw_image: Output image file path
    """

    # ffmpeg -i p1_input1.jpeg -vf format=gray -q:v 10 -y p1_bw1.jpeg
    cmd = [
        "ffmpeg",
        "-i", input_image,
        "-vf", "format=gray",
        "-q:v", str(compression),
        "-y",  # Overwrite output file if it exists
        bw_image
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"B&W image saved to {bw_image}")
    except subprocess.CalledProcessError as e:
        print(f"Error while converting image to B&W: {e}")

# Task 5
def encode_message(message):
# Source: https://www.section.io/engineering-education/run-length-encoding-algorithm-in-python/

    encoded_string = ""
    i = 0
    while (i <= len(message)-1):
        count = 1
        ch = message[i]
        j = i
        while (j < len(message)-1):
            if (message[j] == message[j + 1]):
                count = count + 1
                j = j + 1
            else:
                break
        encoded_string = encoded_string + str(count) + ch
        i = j + 1
    return encoded_string

# Task 6
class DCT:
    def __init__(self, block_size=8):
        self.block_size = block_size

    def encode(self, data):
        return dct(dct(data.T, norm='ortho').T, norm='ortho')

def main():
    print("########## Task 1 ##########")
    if len(sys.argv) != 4:
        print("Usage: python rgb_yuv.py <R_value> <G_value> <B_value>")
        return

    r = int(sys.argv[1])
    g = int(sys.argv[2])
    b = int(sys.argv[3])

    y, u, v = rgb_to_yuv(r, g, b)
    print(f"RGB ({r}, {g}, {b}) to YUV: ({y}, {u}, {v})")

    r2, g2, b2 = yuv_to_rgb(y, u, v)
    print(f"YUV ({y}, {u}, {v}) to RGB: ({r2}, {g2}, {b2})")

    input_image = "p1_input1.jpeg"

    print("########## Task 2 ##########")
    resized_image = "p1_resized1.jpeg"
    resize_image(input_image, resized_image, 200, 300, 10)

    print("########## Task 3 ##########")
    serpentine_seq = serpentine(input_image)
    print(serpentine_seq)

    print("########## Task 4 ##########")
    bw_image = "p1_bw1.jpeg"
    bw(input_image, bw_image, 50)
#As we use a high value of compression, the result image appears very pixelated

    print("########## Task 5 ##########")
    message = "AuuBBBCCCCCCcccccCCCCCCCCCA"
    encoded = encode_message(message)

    print("Original string: [" + message + "]")
    print("Encoded string: [" + encoded + "]")

    print("########## Task 6 ##########")
    data = np.array([4, 3, 5, 10])
    processor = DCT()
    encoded_data = processor.encode(data)

    print("Original Data: " + str(data))
    print("Encoded Data: " + str(encoded_data))

if __name__ == "__main__":
    main()
