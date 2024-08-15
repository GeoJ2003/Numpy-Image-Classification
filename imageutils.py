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
def load_images(dir_path, width=100, height=100, num_images=0):
    images_dict = {}
    count = 0

    for file in os.listdir(dir_path):
        if num_images and count >= num_images:
            break
        img_path = os.path.join(dir_path, file)

        try:
            vectorized_img = load_and_vectorize(img_path, width, height)
            images_dict[file] = vectorized_img
            count += 1

        except IOError:
            print(f"{file} is not a valid image.")

    return images_dict, count

# Write a function for combining the vectorized images into a matrix (2D NumPy array), where every vectorized image is a column
def combine_images(images_dict):
    if not images_dict:
        return np.array([])
    
    combined_matrix = np.column_stack(list(images_dict.values()))
    
    return combined_matrix

def load_and_vectorize(img_path, width=100, height=100):
    img = load_image_and_resize(img_path, width, height)
    img_array = np.array(img) / 255.0
    vectorized_img = vectorize_2D_array(img_array)
    
    # Normalize the vectorized image to have unit norm
    norm = np.linalg.norm(vectorized_img)
    if norm == 0:
        norm = 1  # Avoid division by zero
    vectorized_img_normalized = vectorized_img / norm

    return vectorized_img_normalized