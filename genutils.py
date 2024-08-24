import os
import numpy as np
from PIL import Image

# Function to load MNIST images and labels
def load_mnist_images(filename):
    with open(filename, 'rb') as f:
        f.read(4)  # Skip magic number
        num_images = int.from_bytes(f.read(4), byteorder='big')
        rows = int.from_bytes(f.read(4), byteorder='big')
        cols = int.from_bytes(f.read(4), byteorder='big')
        images = np.fromfile(f, dtype=np.uint8).reshape(num_images, rows, cols)
    return images

def load_mnist_labels(filename):
    with open(filename, 'rb') as f:
        f.read(4)  # Skip magic number
        num_labels = int.from_bytes(f.read(4), byteorder='big')
        labels = np.fromfile(f, dtype=np.uint8)
    return labels

def load_mnist_data():
    # Load MNIST data
    train_images = load_mnist_images('MNIST_ORG/train-images.idx3-ubyte')
    train_labels = load_mnist_labels('MNIST_ORG/train-labels.idx1-ubyte')

    # Create directories for each digit inside imgs/mnist
    mnist_dir = 'imgs/mnist'
    for digit in range(10):
        os.makedirs(os.path.join(mnist_dir, str(digit)), exist_ok=True)

    # Save images into corresponding directories
    for i in range(len(train_images)):
        image = Image.fromarray(train_images[i])
        label = train_labels[i]
        image_path = os.path.join(mnist_dir, str(label), f'image_{i}.jpg')
        image.save(image_path)

def check_directory_structure(base_dir):
    subdirectories = [dir for dir in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, dir))]
    
    if len(subdirectories) < 2:
        return False
    
    valid_subdirs = 0
    for subdir in subdirectories:
        subdir_path = os.path.join(base_dir, subdir)
        images = [file for file in os.listdir(subdir_path) if os.path.isfile(os.path.join(subdir_path, file))]
        if len(images) >= 2:
            valid_subdirs += 1
    
    return valid_subdirs >= 2

def count_images_in_directories(base_dir):
    image_counts = {}
    subdirectories = [dir for dir in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, dir))]
    
    for subdir in subdirectories:
        subdir_path = os.path.join(base_dir, subdir)
        images = [file for file in os.listdir(subdir_path) if os.path.isfile(os.path.join(subdir_path, file))]
        image_counts[subdir] = len(images)
    
    return image_counts