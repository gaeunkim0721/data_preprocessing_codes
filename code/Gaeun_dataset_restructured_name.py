import os
import concurrent.futures
from tqdm import tqdm


# 데이터셋의 루트 경로
dataset_root = '/home/gaeun/HV_plate/datasets/plates_blackened_renamed_full_rotation_leaned_brightness_leaned_translated_leaned_perspective_leaned_stratified'

# 클래스 이름
class_names = ['edge_in_small_hole', 'edge_scratch', 'hole_closed', 'hole_press', 'poke', 'scratch', 'surface_scratch', 'undefined']

# 'train', 'val', 'test' 디렉토리
directories = ['train', 'val', 'test']

# 파일 확장자 설정
image_extensions = ['.jpg', '.jpeg', '.png']
label_extension = '.txt'

# 클래스 번호에 따라 이미지 및 텍스트 파일 이름 변경
def rename_file(dir_path, file):
    filename, file_extension = os.path.splitext(file)
    if file_extension.lower() in image_extensions:
        label_file_path = os.path.join(dir_path, filename + label_extension)
        if os.path.exists(label_file_path):
            with open(label_file_path, 'r') as label_file:
                # 첫 번째 클래스 번호 읽기
                class_num = int(label_file.readline().split()[0])
                class_name = class_names[class_num]  # 클래스 번호에 해당하는 이름

            # 새 파일 이름 생성
            new_filename = f"{class_name}_{filename}"
            new_image_path = os.path.join(dir_path, new_filename + file_extension)
            new_label_path = os.path.join(dir_path, new_filename + label_extension)

            # 파일 이름 변경
            os.rename(os.path.join(dir_path, file), new_image_path)
            os.rename(label_file_path, new_label_path)

# 각 디렉토리의 파일 이름 변경
for directory in directories:
    dir_path = os.path.join(dataset_root, directory)
    files = [f for f in os.listdir(dir_path) if f.endswith(tuple(image_extensions))]
    
    # 병렬 처리
    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(tqdm(executor.map(lambda file: rename_file(dir_path, file), files), total=len(files)))
