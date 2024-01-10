import argparse
import os
from PIL import Image
from tqdm import tqdm

def resize_and_compress(image_path, output_path, base_width, quality):
    with Image.open(image_path) as img:
        # Calculate the height using the aspect ratio
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))

        # Resize the image while maintaining the aspect ratio
        img = img.resize((base_width, h_size), Image.ANTIALIAS)

        # Save the image with the specified quality
        img.save(output_path, quality=quality)

def process_directory(input_dir, output_dir, base_width, quality):
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    for filename in tqdm(files, desc="Processing images"):
        image_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        resize_and_compress(image_path, output_path, base_width, quality)
    
def main():
    input_dir = '/input'
    output_dir = '/output'
    base_width = int(os.environ.get('WIDTH', 800))
    quality = int(os.environ.get('QUALITY', 85))

    process_directory(input_dir, output_dir, base_width, quality)

if __name__ == "__main__":
    main()
