import os
from PIL import Image

def save_image(img_pil, extension='jpg', filename='saved_image', path='imgs/saved_images'):
    img_pil = Image.fromarray(img_pil)
    count = 0
    fullname = f'{filename}.{extension}'
    full_path = os.path.join(path, fullname)

    while True:
        if os.path.exists(full_path):
            count += 1
            fullname = f'{filename}_({count}).{extension}'
            full_path = os.path.join(path, fullname)
        else:
            if not os.path.exists(path):
                os.makedirs(path)
            img_pil.save(full_path)
            print(f"File {filename} saved in {path}.")
            break