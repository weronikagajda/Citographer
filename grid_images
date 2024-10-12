import os
from PIL import Image
import math

folder_name = r"C:\Users\...\scrape_cable"  # Change this to your folder name
output_image = 'image_grid_cable.jpg'  # Change this to the final image name
tile_size = (200, 200)  # ADJUST if you want
background_color = (255, 255, 255)  # ADJUST if you want, it is simply rgb color

image_files = [f for f in os.listdir(folder_name) if f.endswith(('jpg', 'jpeg', 'png'))]
total_images = len(image_files)

# Calculate the grid size 
if total_images > 0:
    grid_size = math.isqrt(total_images)  
    num_images_to_use = grid_size ** 2    

    image_files = image_files[:num_images_to_use]
else:
    print("No images found in the specified folder.")
    exit()

grid_image = Image.new('RGB', (grid_size * tile_size[0], grid_size * tile_size[1]), background_color)

def crop_to_square(img):
    width, height = img.size
    if width == height:
        return img  
    
    if width > height:
        left = (width - height) // 2
        right = left + height
        top = 0
        bottom = height
    else:
        top = (height - width) // 2
        bottom = top + width
        left = 0
        right = width
    return img.crop((left, top, right, bottom))

for index, image_file in enumerate(image_files):
    img_path = os.path.join(folder_name, image_file)
    img = Image.open(img_path)

    img = crop_to_square(img)
    img = img.resize(tile_size)

    x_offset = (index % grid_size) * tile_size[0]
    y_offset = (index // grid_size) * tile_size[1]

    grid_image.paste(img, (x_offset, y_offset))

grid_image.save(output_image)

print(f"Image grid saved as {output_image}")
