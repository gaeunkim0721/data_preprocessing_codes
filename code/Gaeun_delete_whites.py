from PIL import Image, ImageStat
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from functools import partial




def calculate_brightness(image_path):
    """이미지의 평균 밝기를 계산하는 함수"""
    with Image.open(image_path) as img:
        img = img.convert('L')  # Convert to grayscale
        stat = ImageStat.Stat(img)
        return stat.mean[0]

def is_dark_image(file_path, brightness_threshold=50):
    """이미지가 어두운지 확인하는 함수"""
    return calculate_brightness(file_path) < brightness_threshold

def is_bright_image(file_path, brightness_threshold=200):
    """이미지가 밝은지 확인하는 함수"""
    return calculate_brightness(file_path) > brightness_threshold

def process_file(file_path, std_dev_threshold=5, brightness_threshold_low=50, brightness_threshold_high=200):
    """파일 처리 및 필요한 경우 이미지와 라벨 파일 삭제하는 함수"""
    label_file_path = os.path.splitext(file_path)[0] + '.txt'
    # 이미지 파일과 라벨 파일이 모두 존재하는 경우에만 처리
    if os.path.exists(label_file_path):
        if file_path.endswith(('.jpg', '.jpeg', '.png')):
            if is_low_contrast_image(file_path, std_dev_threshold) or is_dark_image(file_path, brightness_threshold_low) or is_bright_image(file_path, brightness_threshold_high):
                return delete_related_files(file_path, label_file_path)
    return None

# 병렬 처리를 위한 process_file 함수에 고정 인자를 설정
fixed_process_file = partial(process_file, std_dev_threshold=5, brightness_threshold_low=50, brightness_threshold_high=200)



def is_low_contrast_image(file_path, std_dev_threshold=5):
    """이미지가 낮은 대비를 가지고 있는지 확인하는 함수"""
    try:
        with Image.open(file_path) as img:
            img = img.convert('L')  # 그레이스케일로 변환
            stat = ImageStat.Stat(img)
            return stat.stddev[0] < std_dev_threshold
    except IOError:
        return False

def delete_related_files(image_path, label_path):
    """이미지 파일과 관련된 라벨 파일을 삭제하는 함수"""
    try:
        os.remove(image_path)
        os.remove(label_path)
        return True  # 삭제 성공을 나타내는 플래그 반환
    except FileNotFoundError:
        return False  # 파일이 이미 삭제되었거나 없는 경우


dataset_dir = '/home/gaeun/HV_plate/datasets'  # 데이터셋 디렉토리 경로

#  모든 이미지 파일과 텍스트 파일 경로 수집
all_file_paths = [os.path.join(root, file) for root, dirs, files in os.walk(dataset_dir) for file in files]
image_paths = [path for path in all_file_paths if path.endswith(('.jpg', '.jpeg', '.png'))]
label_paths = [path for path in all_file_paths if path.endswith('.txt')]


# 병렬 처리
with ThreadPoolExecutor() as executor:
    results = list(executor.map(fixed_process_file, image_paths))


# 혼자 남은 이미지 파일들을 찾아서 삭제
orphaned_images = [path for path in image_paths if not os.path.exists(os.path.splitext(path)[0] + '.txt')]
for orphan in orphaned_images:
    if os.path.exists(orphan):
        os.remove(orphan)

# 혼자 남은 텍스트 라벨 파일들을 찾아서 삭제
orphaned_labels = [path for path in label_paths if not os.path.exists(os.path.splitext(path)[0] + path[-4:])]
for orphan in orphaned_labels:
    if os.path.exists(orphan):
        os.remove(orphan)

# 삭제된 파일 수를 계산
deleted_files_count = sum(1 for result in results if result)

print(f"Deleted {deleted_files_count} low-contrast or improperly bright images and their labels.")

