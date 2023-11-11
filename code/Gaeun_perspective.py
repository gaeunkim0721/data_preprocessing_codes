import os
import cv2
import numpy as np
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def apply_bbox_perspective_transform(text_file_path, M):
    with open(text_file_path, 'r') as f:
        bbox_lines = f.readlines()

    new_bbox_lines = []
    for line in bbox_lines:
        values = line.split()
        class_id, x_min, y_min, x_max, y_max = map(float, values)
        pts = np.array([[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]], dtype=np.float32).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M).reshape(-1, 2)
        new_line = f"{int(class_id)} {' '.join(map(str, dst.flatten()))}"
        new_bbox_lines.append(new_line)

    new_text_file_path = text_file_path.replace('.txt', '_perspective_transformed.txt')
    with open(new_text_file_path, 'w') as f:
        for line in new_bbox_lines:
            f.write(f"{line}\n")

def apply_perspective_transform_to_image(image_path):
    image = cv2.imread(image_path)
    height, width = image.shape[:2]
    pts_src = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)
    pts_dst = np.array([[50, 50], [width - 50, 50], [width - 50, height - 50], [50, height - 50]], dtype=np.float32)
    M = cv2.getPerspectiveTransform(pts_src, pts_dst)
    warped_image = cv2.warpPerspective(image, M, (width, height))
    
    new_image_name = f"{os.path.splitext(image_path)[0]}_perspective_transformed{os.path.splitext(image_path)[1]}"
    cv2.imwrite(new_image_name, warped_image)

    text_file_name = f"{os.path.splitext(image_path)[0]}.txt"
    if os.path.exists(text_file_name):
        apply_bbox_perspective_transform(text_file_name, M)

def apply_perspective_transform_to_directory(directory_path):
    image_files = [os.path.join(root, file)
                   for root, _, files in os.walk(directory_path)
                   for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        list(tqdm(executor.map(apply_perspective_transform_to_image, image_files), total=len(image_files), desc="Applying perspective transform"))

# 사용 예시
directory_path = '/home/gaeun/HV_plate/yolov5/plates_blackened_renamed_full_rotation_leaned_brightness_leaned_translated_leaned'
apply_perspective_transform_to_directory(directory_path)
