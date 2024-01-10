import argparse
import os
import schedule
import time
import hashlib
from PIL import Image
from tqdm import tqdm

def log(string):
    with open("log.txt", 'w') as file:
        file.write(string + "\n")

def get_file_checksum(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
    
def save_checksums(checksums, filename='checksums.txt'):
    with open(filename, 'w') as file:
        for path, checksum in checksums.items():
            file.write(f"{path}:{checksum}\n")

def read_checksums(filename='checksums.txt'):
    checksums = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                path, checksum = line.strip().split(':')
                checksums[path] = checksum
    except FileNotFoundError:
        pass
    return checksums

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
        img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)

        # Determine the format based on the output file extension
        output_format = 'JPEG'  # Default to JPEG
        if output_path.lower().endswith('.png'):
            output_format = 'PNG'
        elif output_path.lower().endswith('.bmp'):
            output_format = 'BMP'
        elif output_path.lower().endswith('.gif'):
            output_format = 'GIF'
        # Add more formats as needed

        # Save the image with the specified quality and format
        img.save(output_path, format=output_format, quality=quality)

def process_directory(input_dir, output_dir, config_dir, base_width, quality):
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    checksum_file = os.path.join(config_dir, "checksums.txt")
    processed_checksums = read_checksums(checksum_file)
    new_checksums = {}

    for filename in tqdm(files, desc="Processing images"):
        file_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, filename)
        if os.path.isfile(file_path):
            checksum = get_file_checksum(file_path)
            if checksum not in processed_checksums.values():
                resize_and_compress(file_path, output_file_path, base_width, quality)
                new_checksums[file_path] = checksum

    save_checksums(new_checksums, checksum_file)
        
def job():
    input_dir = '/input'
    output_dir = '/output'
    config_dir = '/config'
    base_width = int(os.environ.get('WIDTH', 800))
    quality = int(os.environ.get('QUALITY', 85))

    checksum_file = os.path.join(config_dir, "checksums.txt")
    current_file_count = get_file_count(input_dir)
    previous_file_count = read_previous_file_count(checksum_file)

    if current_file_count != previous_file_count:
        process_directory(input_dir, output_dir, config_dir, base_width, quality)
        save_file_count(current_file_count, checksum_file)

def main():
    log("Starting")
    # Read frequency from environment variable, default to 1 hour if not set
    frequency = os.environ.get('FREQUENCY', '1 hour')

    # Parse the frequency and schedule the job
    if 'minute' in frequency:
        schedule.every(int(frequency.split()[0])).minutes.do(job)
    elif 'hour' in frequency:
        schedule.every(int(frequency.split()[0])).hours.do(job)
    # Add more conditions here if needed (e.g., for days, weeks)

    job()
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()   

