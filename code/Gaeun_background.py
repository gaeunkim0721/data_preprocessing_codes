import shutil
import cv2
import numpy as np
import os
import glob


def process_and_save_image(image_path, label_path,output_dir, x):

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (640, 640))
    image = cv2.resize(image, (640, 640))


    binary_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    circles = cv2.HoughCircles(binary_image, cv2.HOUGH_GRADIENT, dp=0.8, minDist=250, param1=45, param2=46, minRadius=250, maxRadius=302)
    
    if circles is None:
        x += 1
        print(x, circles, os.path.basename(image_path))
        save_path = os.path.join('/home/gaeun/HV_plate/yolov5/black', os.path.basename(image_path))
        # 결과 이미지를 저장합니다.
        cv2.imwrite(save_path, image)

    mask = np.zeros_like(gray)
    if circles is not None:
        print(x, circles, os.path.basename(image_path))
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(mask, (i[0], i[1]), i[2], (255, 255, 255), -1)
        
        masked_image = cv2.bitwise_and(image, image, mask=mask)
    else:
        masked_image = image


    #  이미지와 라벨 파일을 같은 출력 디렉토리에 저장
    image_name = os.path.basename(image_path)
    label_name = os.path.basename(label_path)

    
      # 라벨 파일의 경로를 이미지 파일 이름과 .txt 확장자로 설정합니다.
    label_path = label_path.replace("images", "labels").replace(".bmp", ".txt")
    
    image_save_path = os.path.join(output_dir, image_name)
    label_save_path = os.path.join(output_dir, label_name)

    # 결과 이미지를 저장합니다.
    cv2.imwrite(image_save_path, masked_image)

    try:
        shutil.copy(label_path, label_save_path)
    except FileNotFoundError:
        print(f"Warning: Label file not found for {image_path}")



    return x

def process_images_in_directory(input_dir, output_dir):
    # 출력 디렉토리가 없으면 생성합니다.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    x = 0 
    for image_path in glob.glob(os.path.join(input_dir, '**/*.bmp'), recursive=True):
        # 라벨 파일 경로 생성
        label_path = os.path.splitext(image_path)[0] + '.txt'

        # 이미지 및 라벨 파일 처리
        x = process_and_save_image(image_path, label_path, output_dir, x)


# 사용 예시
input_folder_path = '/home/gaeun/Downloads/20231102/'  # 이미지가 있는 폴더 경로
output_folder_path = '/home/gaeun/Downloads/detect_black'  # 마스크된 이미지를 저장할 폴더 경로

process_images_in_directory(input_folder_path, output_folder_path)