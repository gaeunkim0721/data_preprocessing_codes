import os
from collections import defaultdict
from tqdm import tqdm

def count_labels(data_dir):
    label_counts = defaultdict(int)

    # 파일 목록을 먼저 가져와서 tqdm에 전달합니다.
    all_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(data_dir) for f in filenames if f.endswith(".txt")]
    
    for file_path in tqdm(all_files, desc="Processing files"):
        with open(file_path, 'r') as f:
            labels = f.readlines()
            for label in labels:
                label_id = label.split()[0]
                label_counts[label_id] += 1

    return label_counts


def main():
    data_dir = '/home/gaeun/HV_plate/yolov5/plates_blackened_renamed_full_rotation_leaned_brightness_leaned_translated_leaned_perspective_leaned_stratified'

    # 각 레이블의 샘플 수를 계산합니다.
    label_counts = count_labels(data_dir)
    
    if not label_counts:
        print("No labels found.")
        return

    total_samples = sum(label_counts.values())
    average_samples = total_samples / len(label_counts)

    # 평균 샘플 수보다 50% 이하인 레이블을 "부족한" 레이블로 간주합니다.
    threshold = 0.5 * average_samples

    deficient_labels = [label for label, count in label_counts.items() if count < threshold]
    
    # All labels and their sample counts
    print("\n모든 레이블과 그들의 샘플 수:")
    for label, count in label_counts.items():
        print(f"{label}: {count} samples")
    
    print("\n부족한 레이블:")
    for label in deficient_labels:
        print(f"{label}: {label_counts[label]} samples")

if __name__ == '__main__':
    main()