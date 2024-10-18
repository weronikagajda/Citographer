import os
from PIL import Image
import piexif

# Input and output folders
src_folder = r"path_to_your_foldr_with_images"
dst_folder = f"{src_folder}_small_images"

if not os.path.exists(dst_folder):
    os.makedirs(dst_folder)

for filename in os.listdir(src_folder):
    if filename.endswith(('.jpg', '.JPG', '.jpeg', '.png', '.JPEG')):  # Add or modify the file extensions as per your requirement.
        print(f'Processing {filename}...')
        img_path = os.path.join(src_folder, filename)
        img = Image.open(img_path)

        if "exif" in img.info:
            exif_dict = piexif.load(img.info["exif"])

            exif_dict.pop("thumbnail", None)

            if 41729 in exif_dict["Exif"]:
                exif_dict["Exif"][41729] = bytes(exif_dict["Exif"][41729])

            # Resize image
            width, height = img.size
            new_size = (width // 6, height // 6) # you can change the size
            resized_img = img.resize(new_size, Image.LANCZOS)

            # Convert EXIF data back to byte representation
            try:
                exif_bytes = piexif.dump(exif_dict)
            except ValueError as ve:
                print(f'Failed to dump EXIF data for {filename}: {ve}')
                continue

            # Save new image with EXIF data
            new_img_path = os.path.join(dst_folder, filename)
            resized_img.save(new_img_path, exif=exif_bytes)

        else:
            print(f'Image {filename} does not contain EXIF data. Resizing without preserving EXIF data...')
            # Resize image
            width, height = img.size
            new_size = (width // 5, height // 5)
            resized_img = img.resize(new_size, Image.LANCZOS)

            # Save new image without EXIF data
            new_img_path = os.path.join(dst_folder, filename)
            resized_img.save(new_img_path)

print('Finished resizing images.')
