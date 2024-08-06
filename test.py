import numpy as np
import imageutils as img
import classification as cls
import matrixclass as ms

# Only works with greyscale images (2D arrays)
def print_non_zero_values(array):
    for row in array:
            for value in row:
                if value != 0:
                    print(value, end=' ')
                else:
                    print('.', end=' ')
            print()  # Newline after each row

# img_array = img.load_image_and_resize('imgs/dogs/Dog1.png', 100, 100)

# print_non_zero_values(img_array)

# img_array = img.load_image_and_resize('imgs/dogs/Dog1.png', 100, 100)

# img.save_image(img_pil, 'png', 'Dog1_resized')

# img_pil.show()

# dir = 'imgs/dogs'

# imgsDict = img.load_images(dir)

# print(imgsDict)

# imgs_dict = img.load_images('imgs/mnist/seven')

# cos_sim_table = cls.find_image_cosine_similarities(imgs_dict)

# print(cos_sim_table)

# cls.serve_similarity_table(imgs_dict, cos_sim_table)

# seven_subspace = mc.MatrixClass('imgs/mnist/seven')

# cls.project(seven_subspace, 'imgs/mnist/seven/101.jpg')

# Step 1: Create a MatrixClass object
one = ms.MatrixClass('imgs/mnist/one', 'One')
seven = ms.MatrixClass('imgs/mnist/seven', 'Seven')

one.proj_img_onto_subspace('imgs/mnist/seven/10179.jpg')
seven.proj_img_onto_subspace('imgs/mnist/seven/10179.jpg')

print()

one.proj_img_onto_subspace('imgs/mnist/one/1002.jpg')
seven.proj_img_onto_subspace('imgs/mnist/one/1002.jpg')

# print("This is U:", seven_subspace.get_U())
# print("This is S:", seven_subspace.get_S())
# print("This is Vt:", seven_subspace.get_Vt())
# cls.serve_similarity_table(seven_subspace.imgs_dict, seven_subspace.similarities)

