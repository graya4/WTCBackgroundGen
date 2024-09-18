from PIL import Image, ImageFilter, ImageOps
import sys
import cv2 
import numpy as np


def cartoonize (image):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 9)
  color = cv2.bilateralFilter(image, 9, 200, 200)
  cartoon = cv2.bitwise_and(color, color, mask = edges)
  return cartoon

def convert_image_with_arguments(image):
    #MOTION BLUR: https://www.geeksforgeeks.org/opencv-motion-blur-in-python/
    #POSTERIZE: https://www.geeksforgeeks.org/python-pil-imageops-postarize-method/
    #GAUSSIAN BLUR: https://www.geeksforgeeks.org/python-pil-gaussianblur-method/
    modified_image = Image.open(image).convert('RGB')
    blurred_modified_image = modified_image.filter(ImageFilter.GaussianBlur(2))
    posterized_modified_image = ImageOps.posterize(blurred_modified_image, 2)
    #posterized_modified_image.show()
    image_cv = np.array(posterized_modified_image)
    image_cv = image_cv[:, :, ::-1].copy()

    cartoonfilter = cartoonize(image_cv)


    # BLURRING SHIT

    # Create a diagonal blur kernel
    kernel_size = 5   # Change this to adjust the strength of the blur
    kernel = np.zeros((kernel_size, kernel_size), dtype=np.float32)

    # Set diagonal values to 1
    for i in range(kernel_size):
        kernel[i, kernel_size - i - 1] = 1

    # Normalize the kernel
    kernel /= kernel_size

    # Apply the filter using cv2.filter2D
    diagonal_blur = cv2.filter2D(cartoonfilter, -1, kernel)

    #overlaying faded original image over modified image
    modified_image_base = Image.open(image).convert('RGB')
    base_ocv = np.array(modified_image_base)
    base_ocv = base_ocv[:, :, ::-1].copy()

    
    FinalOut = cv2.addWeighted(base_ocv, 0.5, diagonal_blur, 0.7, 0)
    cv2.imwrite('output.jpg', FinalOut) 




if __name__ == '__main__':
    url = sys.argv[1]
    convert_image_with_arguments(url)