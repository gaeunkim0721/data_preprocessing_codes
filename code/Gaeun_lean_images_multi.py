from PIL import Image
import imagehash
import os
import mimetypes
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager
from tqdm import tqdm

def is_image(file_path):
    mime_type, encoding = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('image')

def process_file(args):
    file_path, hash_dict = args
    try:
        with Image.open(file_path) as img:
            hash_value = imagehash.average_hash(img)
            if hash_value in hash_dict:
                os.remove(file_path)
                # Remove the associated txt file
                txt_file_path = file_path.replace('.jpg', '.txt')
                if os.path.exists(txt_file_path):
                    os.remove(txt_file_path)
            else:
                hash_dict[hash_value] = file_path
    except OSError as e:
        os.remove(file_path)  # Delete corrupt image file
        # Remove the associated txt file if the image is corrupt
        txt_file_path = file_path.replace('.jpg', '.txt')
        if os.path.exists(txt_file_path):
            os.remove(txt_file_path)

def find_duplicates(img_folder):
    with Manager() as manager:
        hash_dict = manager.dict()
        file_paths = []

        for dirname, _, filenames in os.walk(img_folder):
            file_paths.extend([(os.path.join(dirname, filename), hash_dict) for filename in filenames if is_image(os.path.join(dirname, filename))])

        with ProcessPoolExecutor() as executor:
            list(tqdm(executor.map(process_file, file_paths), total=len(file_paths)))

        # The following code for orphaned text files removal is now redundant because
        # we are already deleting the .txt files with their respective images
        # So, we can safely skip or remove this part

if __name__ == '__main__':
    img_folder = '/home/gaeun/HV_plate/yolov5/renamed_rotated'
    find_duplicates(img_folder)