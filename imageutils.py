import os
import numpy as np
from PIL import Image

# Create a utility for loading an image file into a 2D array of gray pixel values in range [0, 255] , as a 2D NumPy array.  
# Use PIL image library for Python for dissecting the image. Include params to resize the image as desired
def load_image_and_resize(image_path, width=100, height=100):

    img = Image.open(image_path).resize((width, height))
    img_gray = img.convert('L')
    img_array = np.array(img_gray)
    
    return img_array

# Write a function for vectorizing the 2D array into a single column vector (column vector should be a 2D NumPy array, with a single column, 
# to facilitate multiplication by a matrix)
def vectorize_2D_array(array):
    return array.reshape(-1, 1)

# Write a function for loading a directory full of JPEG image files into a dict mapping : filename -> vectorized image
def load_images(dir_path):
    images_dict = {}

    for file in os.listdir(dir_path):
        img_path = os.path.join(dir_path, file)

        try:
            # Using default width and height from load_image_and_resize
            img = load_image_and_resize(img_path)
            img_array = np.array(img) / 255.0
            vectorized_img = vectorize_2D_array(np.round(img_array, 2))
            images_dict[file] = vectorized_img

        except IOError:
            print(f"{file} is not a valid image.")

    return images_dict

# Write a function for combining the vectorized images into a matrix (2D NumPy array), where every vectorized image is a column
def combine_images(images_dict):
    if not images_dict:
        return np.array([])
    
    combined_matrix = np.column_stack(list(images_dict.values()))
    
    return combined_matrix