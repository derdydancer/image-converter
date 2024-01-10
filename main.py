import argparse
import os
import schedule
import time
from PIL import Image
from tqdm import tqdm

def get_file_count(directory):
    return len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

def save_file_count(file_count, filename='file_count.txt'):
    with open(filename, 'w') as file:
        file.write(str(file_count))

def read_previous_file_count(filename='file_count.txt'):
    try:
        with open(filename, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return -1
        
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
def job():
    input_dir = '/input'
    output_dir = '/output'
    base_width = int(os.environ.get('WIDTH', 800))
    quality = int(os.environ.get('QUALITY', 85))

    current_file_count = get_file_count(input_dir)
    previous_file_count = read_previous_file_count()

    if current_file_count != previous_file_count:
        process_directory(input_dir, output_dir, base_width, quality)
        save_file_count(current_file_count)

def main():
    # Read frequency from environment variable, default to 1 hour if not set
    frequency = os.environ.get('FREQUENCY', '1 hour')

    # Parse the frequency and schedule the job
    if 'minute' in frequency:
        schedule.every(int(frequency.split()[0])).minutes.do(job)
    elif 'hour' in frequency:
        schedule.every(int(frequency.split()[0])).hours.do(job)
    # Add more conditions here if needed (e.g., for days, weeks)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()   

