import cv2
import numpy as np
import os
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

def adjust_brightness_save(img_path):
    # 이미지 불러오기
    image = cv2.imread(img_path)
    # 기존 이미지의 평균 밝기 계산
    original_brightness = np.mean(image)
    
    # txt 파일의 이름을 만들기 위한 기본 경로 설정
    txt_basepath = os.path.splitext(img_path)[0]
    txt_filename = os.path.basename(txt_basepath) + ".txt"
    txt_filepath = txt_basepath + ".txt"

    for value in range(int(original_brightness) - 20, int(original_brightness) + 20):
        # 밝기 조절이 음수가 되거나 255를 초과하지 않도록 함
        if value < 0 or value > 255:
            continue
        
        # 생성될 이미지의 경로 확인
        filename, ext = os.path.splitext(os.path.basename(img_path))
        new_filename = f"{filename}_{value}{ext}"
        new_filepath = os.path.join(os.path.dirname(img_path), new_filename)
        
        # 이미 생성된 이미지 또는 txt 파일은 건너뛰기
        new_txt_filepath = os.path.splitext(new_filepath)[0] + ".txt"
        if os.path.exists(new_filepath) or os.path.exists(new_txt_filepath):
            continue
        
         # 밝기 조절
        adjusted_value = value - int(original_brightness)  # 이 부분이 변경되었습니다
        M = np.ones(image.shape, dtype="uint8") * adjusted_value
        if image.dtype != M.dtype:
            M = M.astype(image.dtype)
        brightened = cv2.add(image, M)        
        # 조절된 이미지 저장
        cv2.imwrite(new_filepath, brightened)

        # 해당 이미지의 밝기 조절값에 맞는 txt 파일명 생성
        new_txt_filename = f"{filename}_{value}.txt"  # 이 부분을 수정했습니다.
        new_txt_filepath = os.path.join(os.path.dirname(img_path), new_txt_filename)

        # 이미지에 대응하는 txt 파일 저장 또는 복사
        if os.path.exists(txt_filepath):
            # 원본 txt 파일이 있는 경우, 새로운 txt 파일에 내용 복사
            with open(txt_filepath, 'r') as original_txt_file:
                txt_data = original_txt_file.read()
            with open(new_txt_filepath, 'w') as new_txt_file:
                new_txt_file.write(txt_data)
        else:
            # 원본 txt 파일이 없는 경우, 빈 txt 파일 생성
            open(new_txt_filepath, 'a').close()


def process_directory(directory, num_workers=4):
    img_paths = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(('.png', '.jpg', '.bmp')):
                img_paths.append(os.path.join(dirpath, filename))

    # tqdm으로 진행 표시줄 추가
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        list(tqdm(executor.map(adjust_brightness_save, img_paths), total=len(img_paths), desc="Processing images"))

if __name__ == '__main__':
    img_folder = '/home/gaeun/HV_plate/yolov5/renamed_rotated_brightness'
    process_directory(img_folder)
