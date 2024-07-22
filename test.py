import numpy as np
import imageutils as img
import classification as cls

# Only works with greyscale images (2D arrays)
def print_non_zero_values(array):
    for row in array:
            for value in row:
                if value != 0:
                    print(value, end=' ')
                else:
                    print('.', end=' ')
            print()  # Newline after each row

# np.set_printoptions(threshold=np.inf)

# img_array = img.load_image_and_resize('imgs/dogs/Dog1.png', 100, 100)

# print_non_zero_values(img_array)

# img_array = img.load_image_and_resize('imgs/dogs/Dog1.png', 100, 100)

# img.save_image(img_pil, 'png', 'Dog1_resized')

# img_pil.show()

# dir = 'imgs/dogs'

# imgsDict = img.load_images(dir)

# print(imgsDict)

imgs_dict = img.load_images('imgs/mnist')

cos_sim_table = cls.find_image_cosine_similarities(imgs_dict)

cls.serve_similarity_table(imgs_dict, cos_sim_table)