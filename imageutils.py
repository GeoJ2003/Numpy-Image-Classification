import os
import numpy as np
from PIL import Image

# Create a utility for loading an image file into a 2D array of gray pixel values in range [0, 255] , as a 2D NumPy array.  
# Use PIL image library for Python for dissecting the image. Include params to resize the image as desired
def load_image_and_resize(image_path, width, height):

    img = Image.open(image_path)
    img_resized = img.resize((width, height))
    img_gray = img_resized.convert('L')
    img_array = np.array(img_gray)
    
    return img_array

# Write a function for vectorizing the 2D array into a single column vector (column vector should be a 2D NumPy array, with a single column, to facilitate multiplication by a matrix)
def vectorize_2D_array(array):
    column_vector = array.reshape(-1, 1)
    return column_vector

# Write a function for loading a directory full of JPEG image files into a dict mapping : filename -> vectorized image
def load_images(dir_path):
    images_dict = {}

    for file in os.listdir(dir_path):
        img_path = os.path.join(dir_path, file)

        try:
            img = Image.open(img_path)
            img_array = np.array(img)
            vectorized_img = vectorize_2D_array(img_array)
            images_dict[file] = vectorized_img

        except IOError:
            print(f"{file} is not a valid image.")

    return images_dict

# Write a function for combining the vectorized images into a matrix (2D NumPy array), where every vectorized image is a column
def combine_images(vectorized_images):
    if not vectorized_images:
        return np.array([])
    
    num_rows = max(len(img) for img in vectorized_images) # Find longest vector
    num_cols = len(vectorized_images)  # Num of images

    combined_matrix = np.zeros((num_rows, num_cols))
    
    # Fill the matrix with vectorized images
    for col_index, img in enumerate(vectorized_images):
        # Determine the length of the current image vector
        length = len(img)
        # Fill the corresponding column in the matrix
        combined_matrix[:length, col_index] = img
    
    return combined_matrix

def save_image(img_pil, extension):
    path = 'imgs/saved_images'
    counter = 0
    filename = f'saved_image({counter}).{extension}'
    full_path = os.path.join(path, filename)

    while True:
        if os.path.exists(full_path):
            counter += 1
            filename = f'saved_image({counter}).{extension}'
            full_path = os.path.join(path, filename)
        else:
            if not os.path.exists(path):
                os.makedirs(path)
            img_pil.save(full_path)
            print(f"File {filename} saved in {path}.")
            break