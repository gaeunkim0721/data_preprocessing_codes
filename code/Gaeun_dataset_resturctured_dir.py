import os
import shutil
from sklearn.model_selection import train_test_split

# 데이터셋 루트 폴더 및 클래스 리스트
dataset_root = '/home/gaeun/HV_plate/datasets/plates_blackened_renamed_full_rotation_leaned_brightness_leaned_translated_leaned_perspective_leaned_stratified'
class_names = ['edge_in_small_hole', 'edge_scratch', 'hole_closed', 'hole_press', 'poke', 'scratch', 'surface_scratch', 'undefined']

# 분할 비율 설정
train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1

# 파일 분할 및 이동 함수
def split_and_move_files(files, labels, dst_dir, cls):
    train_files, test_files, train_labels, test_labels = train_test_split(files, labels, test_size=(1 - train_ratio), stratify=labels)
    val_files, test_files, val_labels, test_labels = train_test_split(test_files, test_labels, test_size=test_ratio/(test_ratio + val_ratio), stratify=test_labels)

    for file in train_files + val_files + test_files:
        # 이미지 파일과 텍스트 파일의 이름을 추출
        base_name = os.path.basename(file)
        txt_name = os.path.splitext(base_name)[0] + '.txt'

        if file in train_files:
            subdir = 'train'
        elif file in val_files:
            subdir = 'val'
        else:
            subdir = 'test'

        # 이미지 파일 이동
        shutil.move(file, os.path.join(dst_dir, subdir, cls, base_name))
        # 동일한 이름의 텍스트 파일 이동
        shutil.move(os.path.join(os.path.dirname(file), txt_name), os.path.join(dst_dir, subdir, cls, txt_name))

# 디렉토리 구조 생성
for dir_type in ['train', 'val', 'test']:
    for cls in class_names:
        os.makedirs(os.path.join(dataset_root, dir_type, cls), exist_ok=True)

# 파일 분할 및 이동
for cls in class_names:
    cls_files = []
    for root, dirs, files in os.walk(dataset_root):
        for file in files:
            if file.startswith(cls) and file.endswith(('.jpg', '.jpeg', '.png')):
                cls_files.append(os.path.join(root, file))

    if cls_files:
        labels = [cls] * len(cls_files)
        split_and_move_files(cls_files, labels, dataset_root, cls)
    else:
        print(f"No files found for class {cls} in {dataset_root}")
