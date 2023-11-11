import re
from PIL import Image
import os
import shutil

def clean_filename(filename):
    # 정규 표현식을 사용하여 'rf.<32자리 hex>.' 패턴을 찾아 제거합니다.
    pattern = re.compile(r'rf\.[0-9a-f]{32}\.')
    return pattern.sub('', filename)

def resize_image(input_image_path, output_image_path):
    try:
        with Image.open(input_image_path) as img:
            img = img.resize((640, 640), Image.LANCZOS)
            img.save(output_image_path)
            print(f"Resized image saved to {output_image_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def find_and_resize_images(source_directory, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            clean_name = clean_filename(file)  # 파일 이름 정리
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                input_image_path = os.path.join(root, file)
                output_image_path = os.path.join(target_directory, clean_name)  # 정리된 이름 사용
                resize_image(input_image_path, output_image_path)
            elif file.lower().endswith('.txt'):
                # 라벨 파일도 동일한 로직으로 이름을 정리하고 복사
                base_name = os.path.splitext(clean_name)[0]
                input_label_path = os.path.join(root, file)
                output_label_path = os.path.join(target_directory, base_name + '.txt')
                shutil.copy(input_label_path, output_label_path)
                print(f"Label file copied to {output_label_path}")

# 'source_directory_path'를 이미지가 있는 원본 디렉토리 경로로 교체하세요
# 'target_directory_path'를 리사이징된 이미지와 라벨 파일을 저장할 새로운 디렉토리 경로로 교체하세요
source_directory_path = '/home/gaeun/Downloads/plates.v6i.yolov5pytorch'
target_directory_path = '/home/gaeun/Downloads/resized_images'
find_and_resize_images(source_directory_path, target_directory_path)