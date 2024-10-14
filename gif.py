import os
from PIL import Image

folder_name = r'C:\Users\...\scrape_cable'  # Change this to your folder name
output_gif = 'gif_cable.gif'  # Name of the output GIF
tile_size = (200, 200)  
duration_per_frame = 500  # Duration per frame in milliseconds (500 ms = 0.5 seconds)
loop_count = 0  # infinite loop 

image_files = [f for f in os.listdir(folder_name) if f.endswith(('jpg', 'jpeg', 'png'))]

images = []
for image_file in image_files:
    img_path = os.path.join(folder_name, image_file)
    img = Image.open(img_path)

    img.thumbnail(tile_size)

    background = Image.new('RGB', tile_size, (0, 0, 0))  # Black background, adjust if you want 
    background.paste(img, ((tile_size[0] - img.width) // 2, (tile_size[1] - img.height) // 2))

    images.append(background)

images[0].save(output_gif, save_all=True, append_images=images[1:], duration=duration_per_frame, loop=loop_count)

print(f"GIF saved as {output_gif}")
