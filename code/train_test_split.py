import os
import shutil
from sklearn.model_selection import train_test_split

data_dir = '/mnt/external/augment0_lean_brightness/results'
train_dir = os.path.join(data_dir, 'train')
val_dir = os.path.join(data_dir, 'val')
test_dir = os.path.join(data_dir, 'test')

os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# 재귀적으로 모든 이미지 파일과 라벨 파일을 찾습니다.
image_extensions = {'.bmp', '.png'}
label_files = {}
image_files = []

for subdir, dirs, files in os.walk(data_dir):
    for file in files:
        filepath = os.path.join(subdir, file)
        filebase, extension = os.path.splitext(file)
        if extension.lower() in image_extensions:
            image_files.append(filepath)
        elif extension.lower() == '.txt':
            label_files[filebase] = filepath

paired_files = []
labels = []
for image_path in image_files:
    base_name = os.path.basename(image_path).rsplit('.', 1)[0]
    label_path = label_files.get(base_name)
    if label_path:
        with open(label_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                class_label = line.split()[0]
                labels.append(class_label)
                paired_files.append((image_path, label_path))
                break

# paired_files와 labels에 데이터가 있는지 확인합니다.
if not paired_files or not labels:
    raise ValueError("No data to split. Check the contents of 'paired_files' and 'labels'.")

# 데이터를 분할합니다.
_, test_files, _, test_labels = train_test_split(paired_files, labels, test_size=0.1, stratify=labels)
train_files, val_files, train_labels, val_labels = train_test_split(paired_files, labels, test_size=0.125, stratify=labels)

# 파일을 이동하는 함수입니다.
def move_files(file_tuples, destination):
    for img_path, label_path in file_tuples:
        # 이미지 파일의 존재 여부를 확인하고 이동합니다.
        if os.path.exists(img_path):
            shutil.move(img_path, os.path.join(destination, os.path.basename(img_path)))
        else:
            print(f"File not found, skipping: {img_path}")

        # 라벨 파일의 존재 여부를 확인하고 이동합니다.
        if os.path.exists(label_path):
            shutil.move(label_path, os.path.join(destination, os.path.basename(label_path)))
        else:
            print(f"File not found, skipping: {label_path}")

# 파일들을 이동시킵니다.
move_files(train_files, train_dir)
move_files(val_files, val_dir)
move_files(test_files, test_dir)

# 세트의 크기를 출력합니다.
print(f"Number of training files: {len(train_files)}")
print(f"Number of validation files: {len(val_files)}")
print(f"Number of test files: {len(test_files)}")
