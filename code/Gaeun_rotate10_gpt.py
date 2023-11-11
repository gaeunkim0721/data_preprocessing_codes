import cv2
import numpy as np
import os
import glob
from tqdm import tqdm
from multiprocessing import Pool, cpu_count


def bbox_to_yolo_format(rotated_bbox, img_width, img_height):
    x1, y1, x2, y2 = rotated_bbox
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    width = x2 - x1
    height = y2 - y1
    return center_x / img_width, center_y / img_height, width / img_width, height / img_height


def yolo_format_to_bbox(yolo_label, img_width, img_height):
    center_x, center_y, width, height = yolo_label
    x1 = (center_x - width / 2) * img_width
    y1 = (center_y - height / 2) * img_height
    x2 = (center_x + width / 2) * img_width
    y2 = (center_y + height / 2) * img_height
    return [(x1, y1), (x2, y2)]


def get_initial_bbox(label_path, img_width, img_height):
    bboxes = []
    with open(label_path, 'r') as label_file:
        lines = label_file.readlines()
        for line in lines:
            class_id, center_x, center_y, width, height = map(float, line.strip().split())
            yolo_label = (center_x, center_y, width, height)
            bbox = yolo_format_to_bbox(yolo_label, img_width, img_height)
            bboxes.append((class_id, bbox))
    return bboxes

def rotate_image_and_bbox(img, bbox, angle):
    rows, cols = img.shape[:2]
    center = (cols / 2, rows / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
    
    # 이미지 회전
    rotated_img = cv2.warpAffine(img, rotation_matrix, (cols, rows))
    
    # 바운딩 박스 회전
    bbox_points = np.float32([
        [bbox[0][0], bbox[0][1]],
        [bbox[1][0], bbox[0][1]],
        [bbox[1][0], bbox[1][1]],
        [bbox[0][0], bbox[1][1]]
    ])
    rotated_bbox_points = cv2.transform(np.array([bbox_points]), rotation_matrix)[0]
    rotated_bbox = [
        min(rotated_bbox_points[:, 0]),
        min(rotated_bbox_points[:, 1]),
        max(rotated_bbox_points[:, 0]),
        max(rotated_bbox_points[:, 1])
    ]
    
    return rotated_img, rotated_bbox


def rotate_and_save(args):
    img, bboxes, i, image_name, save_dir = args
    angle = i * 10
    rotated_imgs_and_bboxes = [rotate_image_and_bbox(img, bbox, angle) for class_id, bbox in bboxes]
    rotated_img = rotated_imgs_and_bboxes[0][0]
    save_path = os.path.join(save_dir, f'{image_name}_rotated_{angle}.jpg')
    cv2.imwrite(save_path, rotated_img)

    label_path = os.path.join(save_dir, f'{image_name}_rotated_{angle}.txt')
    with open(label_path, 'w') as label_file:
        for j, (rotated_img, rotated_bbox) in enumerate(rotated_imgs_and_bboxes):
            class_id, _ = bboxes[j]
            yolo_label = bbox_to_yolo_format(rotated_bbox, img.shape[1], img.shape[0])
            label_file.write(f'{int(class_id)} {yolo_label[0]} {yolo_label[1]} {yolo_label[2]} {yolo_label[3]}\n')




def rotate_images_in_folder_recursive(folder_path, save_dir, rotations=360):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 이미지 파일 검색
    image_paths = glob.glob(os.path.join(folder_path, '*.jpg'))
    
    for image_path in tqdm(image_paths, desc="Processing images"):
        img = cv2.imread(image_path)
        image_name = os.path.basename(image_path).split('.')[0]
        
         
        # 라벨 파일 경로 수정
        label_folder_path = folder_path.replace('images', 'labels')  # 예시: 'images'를 'labels'로 변경
        label_path = os.path.join(label_folder_path, f'{image_name}.txt')

        bboxes = get_initial_bbox(label_path, img.shape[1], img.shape[0])

        # 병렬 처리를 위한 인자 설정
        args = [(img, bboxes, i, image_name, save_dir) for i in range(0, rotations)]
        
        # 병렬 처리 시작
        with Pool(cpu_count()) as p:
            p.map(rotate_and_save, args)
        
        # for i in range(0, rotations):  # 각도가 10도씩 증가하도록 수정된 부분
        #     angle = i  # 각도가 10도씩 증가하도록 수정된 부분
        #     rotated_imgs_and_bboxes = [rotate_image_and_bbox(img, bbox, angle) for class_id, bbox in bboxes]  # 수정된 부분
        #     # 첫 번째 이미지만 사용하여 저장합니다 (모든 이미지는 동일하게 회전됩니다).
        #     rotated_img = rotated_imgs_and_bboxes[0][0]
        #     save_path = os.path.join(save_dir, f'{image_name}_rotated_{angle}.bmp')
        #     cv2.imwrite(save_path, rotated_img)
            
        #     label_path = os.path.join(save_dir, f'{image_name}_rotated_{angle}.txt')
        #     with open(label_path, 'w') as label_file:
        #         for j, (rotated_img, rotated_bbox) in enumerate(rotated_imgs_and_bboxes):
        #             class_id, _ = bboxes[j]
        #             yolo_label = bbox_to_yolo_format(rotated_bbox, img.shape[1], img.shape[0])
        #             label_file.write(f'{int(class_id)} {yolo_label[0]} {yolo_label[1]} {yolo_label[2]} {yolo_label[3]}\n')
    
    # 재귀적으로 서브 폴더 검색
    sub_folders = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
    for sub_folder in sub_folders:
        rotate_images_in_folder_recursive(os.path.join(folder_path, sub_folder), os.path.join(save_dir, sub_folder), rotations)

folder_path = '/home/gaeun/HV_plate/yolov5/renamed'
save_dir = '/home/gaeun/HV_plate/yolov5/renamed_rotated'

rotate_images_in_folder_recursive(folder_path, save_dir)