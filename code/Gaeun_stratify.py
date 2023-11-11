import os
import shutil
from sklearn.model_selection import train_test_split

from collections import Counter

def count_labels_in_directory(directory):
    label_counts = Counter()
    # 디렉토리 내의 모든 .txt 파일을 찾아서 라벨 수를 계산합니다.
    for label_file in os.listdir(directory):
        if label_file.endswith('.txt'):
            with open(os.path.join(directory, label_file), 'r') as file:
                for line in file:
                    class_label = line.split()[0]
                    label_counts[class_label] += 1
    return label_counts


data_dir = '/home/gaeun/HV_plate/yolov5/plates_blackened_renamed_full_rotation_leaned_brightness_leaned_translated_leaned_perspective_leaned'
train_dir = os.path.join(data_dir, 'train')
val_dir = os.path.join(data_dir, 'val')
test_dir = os.path.join(data_dir, 'test')

# 필요한 디렉토리를 생성합니다.
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# 이미지와 라벨 파일을 수집합니다.
image_files = []
label_files = {}

for dp, dn, filenames in os.walk(data_dir):
    for f in filenames:
        if f.endswith('.bmp') or f.endswith('.jpg'):
            image_files.append(os.path.join(dp, f))
        elif f.endswith('.txt'):
            base_name = os.path.splitext(f)[0]
            label_files[base_name] = os.path.join(dp, f)

# 이미지와 라벨 파일을 짝지어줍니다.
paired_files = []
labels = []
for img_file in image_files:
    base_name = os.path.splitext(os.path.basename(img_file))[0]
    if base_name in label_files:
        with open(label_files[base_name], 'r') as file:
            lines = file.readlines()
            for line in lines:
                class_label = line.split()[0]
                labels.append(class_label)
                paired_files.append((img_file, label_files[base_name]))
                break  # 가정: 한 이미지에 하나의 라벨만 존재합니다.

# 데이터가 없으면 여기서 중단합니다.
if not paired_files or not labels:
    print("No paired image-label files found. Please check the dataset.")
else:
    # 전체 데이터 세트를 80% 훈련, 20% 나머지(검증+테스트)로 분할합니다.
    train_files, remaining_files, train_labels, remaining_labels = train_test_split(
        paired_files, labels, test_size=0.2, stratify=labels
    )

    # 나머지 데이터를 50% 검증, 50% 테스트로 분할합니다.
    val_files, test_files, val_labels, test_labels = train_test_split(
        remaining_files, remaining_labels, test_size=0.5, stratify=remaining_labels
    )

    # 파일을 이동하는 함수를 정의합니다.
    def move_files(file_tuples, destination):
        for img_file, label_file in file_tuples:
            # 파일의 새 위치를 결정합니다.
            new_img_path = os.path.join(destination, os.path.basename(img_file))
            new_label_path = os.path.join(destination, os.path.basename(label_file))
            
            # 파일을 새 위치로 이동합니다.
            shutil.move(img_file, new_img_path)
            shutil.move(label_file, new_label_path)

    # 파일을 각각의 디렉토리로 이동합니다.
    move_files(train_files, train_dir)
    move_files(val_files, val_dir)
    move_files(test_files, test_dir)



# 각 디렉토리의 라벨 수를 계산합니다.
train_label_counts = count_labels_in_directory(train_dir)
val_label_counts = count_labels_in_directory(val_dir)
test_label_counts = count_labels_in_directory(test_dir)

# 결과를 출력합니다.
print("Train label counts:", train_label_counts)
print("Validation label counts:", val_label_counts)
print("Test label counts:", test_label_counts)