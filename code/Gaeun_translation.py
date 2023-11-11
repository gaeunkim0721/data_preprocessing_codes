import os
from PIL import Image
import random
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import numpy as np


def translate_bbox(bbox, translate_x, translate_y, img_width, img_height):
    """
    Translate a bounding box in YOLO format.
    YOLO format: (center_x, center_y, width, height) with normalized values.
    """
    center_x, center_y, width, height = bbox
    translated_x = center_x + (translate_x / img_width)
    translated_y = center_y + (translate_y / img_height)
    
    # Ensure the translated bounding box does not go out of image boundaries
    translated_x = min(max(translated_x, width / 2), 1 - width / 2)
    translated_y = min(max(translated_y, height / 2), 1 - height / 2)

    return translated_x, translated_y, width, height

def translate_image(image, translate_x, translate_y):
    """
    Translate an image by a certain number of pixels.
    """
    translation_matrix = np.float32([[1, 0, translate_x], [0, 1, translate_y]])
    translated_image = image.transform(
        image.size,
        Image.AFFINE,
        translation_matrix.flatten()[:6],
        resample=Image.BICUBIC
    )
    return translated_image

def random_translate_image(image_path, max_translation):
    """
    Apply a random translation to an image.
    """
    try:
        with Image.open(image_path) as image:
            translate_x = random.randint(-max_translation, max_translation)
            translate_y = random.randint(-max_translation, max_translation)
            translated_image = translate_image(image, translate_x, translate_y)
            return translated_image, translate_x, translate_y, image_path
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None, None, None, image_path

def save_translated_image_and_bbox(image_data, max_translation, img_width, img_height):
    """
    Save the translated image and update bounding box coordinates.
    """
    translated_image, tx, ty, image_path = image_data
    if translated_image:
        # Construct new file names
        file_name = os.path.basename(image_path)
        image_base_name = os.path.splitext(file_name)[0]
        new_image_name = f"{image_base_name}_translated_{tx}_{ty}.jpg"
        new_image_path = os.path.join(os.path.dirname(image_path), new_image_name)

        # Save the translated image
        translated_image.save(new_image_path)

        # If there's a corresponding bounding box file, update it
        text_file_name = f"{image_base_name}.txt"
        text_file_path = os.path.join(os.path.dirname(image_path), text_file_name)
        new_text_file_name = f"{image_base_name}_translated_{tx}_{ty}.txt"
        new_text_file_path = os.path.join(os.path.dirname(image_path), new_text_file_name)

        if os.path.exists(text_file_path):
            with open(text_file_path, 'r') as original, open(new_text_file_path, 'w') as new_file:
                for line in original:
                    elements = line.split()
                    bbox = tuple(map(float, elements[1:]))
                    translated_bbox = translate_bbox(bbox, tx, ty, img_width, img_height)
                    new_file.write(f"{elements[0]} {' '.join(map(str, translated_bbox))}\n")

def process_images(image_paths, max_translation):
    """
    Process all images to apply random translation.
    """
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(random_translate_image, p, max_translation) for p in image_paths]
        results = []
        for future in tqdm(futures, total=len(image_paths)):
            result = future.result()
            if result[0]:  # If the image was successfully translated
                img_width, img_height = result[0].size
                save_translated_image_and_bbox(result, max_translation, img_width, img_height)
            results.append(result)

def apply_random_translation_to_directory(directory_path, max_translation=10):
    """
    Apply random translation to all images in a directory.
    """
    image_paths = [os.path.join(root, file)
                   for root, _, files in os.walk(directory_path)
                   for file in files
                   if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    process_images(image_paths, max_translation)

# Usage example
apply_random_translation_to_directory('/home/gaeun/HV_plate/yolov5/plates_blackened_renamed_full_rotation_leaned_brightness_leaned')
