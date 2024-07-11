import imageutils as img

# Load and resize the image, then convert it back to a PIL image
img_array = img.load_image_and_resize('imgs/dogs/Dog1.png', 100, 100)
img_pil = img.Image.fromarray(img_array)

# Save the image
img.save_image(img_pil, 'png', 'Dog1_resized')

# Display the image
img_pil.show()

# dir = 'imgs/dogs'

# imgsDict = img.load_images(dir)

# print(imgsDict)