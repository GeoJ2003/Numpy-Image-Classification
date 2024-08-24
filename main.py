import genutils as gen
import matrixclass as mc
import os

if __name__ == "__main__":
    imgs_dir = "imgs"
    directories = [dir for dir in os.listdir(imgs_dir) if os.path.isdir(os.path.join(imgs_dir, dir))]

    if 'mnist' not in directories:
        while True:
            response = input("The mnist directory is currently not in the 'imgs' directory. Would you like to add it? (y/n): ")
            if response.lower() == 'y':
                gen.load_mnist_data()
                directories.append('mnist')
                break
            elif response.lower() == 'n':
                break
            else:
                print("Invalid response. Please enter 'y' or 'n'.")

    dir_selection = None
    dir_dict = []

    while True:
        print("Available Directories:", directories)
        response = input("Which directory would you like to use for classification? ")
        if response in directories:
            dir_selection = response
            dir_dict = gen.count_images_in_directories(os.path.join(imgs_dir, dir_selection))
            print(f"Images in {dir_selection} directory:", dir_dict)
            break
        else:
            print("Invalid directory. Please choose a valid directory.")

    selected_dirs = {}

    while True:
        response = input("Which directories would you like to use for image classification? ")
        valid = True
        for dir in response.split(','):
            dir = dir.strip()
            if dir in dir_dict:
                selected_dirs[dir] = dir_dict[dir]
            else:
                print(f"{dir} is not a valid directory. Please choose a valid directory.")
                valid = False
        if valid:
            break
    
    excluded_dirs = [dir for dir in dir_dict if dir not in selected_dirs]

    threshold = 0.01
    # Optional
    while True:
        response = input("Would you like to change the threshold? (default is 0.01) (y/n): ")
        if response.lower() == 'y':
            threshold = float(input("Enter the threshold: "))
            if not threshold.isdigit():
                print("Invalid input. Please enter a valid number.")
            elif float(threshold) < 0 or float(threshold) > 1:
                print("Threshold must be between 0 and 1.")
            else:
                break
        if response.lower() == 'n':
            break


    width = 100
    height = 100

    # Optional
    while True:
        response = input("Would you like to re-size each image? (default is 100x100) (y/n): ")
        if response.lower() == 'y':
            width = int(input("Enter the width: "))
            height = int(input("Enter the height: "))
            break
        if response.lower() == 'n':
            break

    training_images = 1
    max_images_to_choose = min(selected_dirs.values()) - 1

    while True:
        response = input(f"Select a # of images less than or equal to {max_images_to_choose} to use for training: ")

        if not response.isdigit():
            print("Invalid input. Please enter a valid number.")
            continue
        elif response.isdigit() and int(response) < max_images_to_choose:
            training_images = int(response)
            break
        else:
            print("Selected # of images exceeds the number of images in the smallest directory. Please choose a smaller number.")

    print(f"Creating subspaces using {training_images} images from each directory...")

    dir_path = os.path.join(imgs_dir, dir_selection)
    matrix_classes = mc.MC_list(dir_path, training_images, excluded_dirs, threshold, width, height)

    images_to_classify = 1
    max_images_to_choose = min(selected_dirs.values()) - training_images

    while True:
        response = input(f"Select a # of images less than or equal to {max_images_to_choose} to classify: ")

        if not response.isdigit():
            print("Invalid input. Please enter a valid number.")
            continue
        elif response.isdigit() and int(response) < max_images_to_choose:
            images_to_classify = int(response)
            break
        else:
            print("Selected # of images exceeds the number of images that can be classified in the smallest directory. Please choose a smaller number.")

    print(f"Classifying {images_to_classify} images from each directory...")
    matrix_classes.classify_dirs(dir_path, images_to_classify)

    
    