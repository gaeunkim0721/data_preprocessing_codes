import os

# Function to rename files by removing a specified part and everything that follows it
def rename_and_clean_files(directory, part_to_remove):
    renamed_files_info = []
    # os.walk를 사용하여 디렉토리 내의 모든 파일에 대해 순회합니다.
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            if part_to_remove in file:
                # 파일명과 확장자를 분리합니다.
                name, ext = os.path.splitext(file)
                # 지정된 부분을 제거합니다.
                new_name_base = name.split(part_to_remove)[0]
                new_name = new_name_base + ext
                # 새 파일 경로를 생성합니다.
                new_file_path = os.path.join(dirpath, new_name)
                # 원래 파일 경로를 생성합니다.
                original_file_path = os.path.join(dirpath, file)
                # 파일 이름을 변경합니다.
                os.rename(original_file_path, new_file_path)
                # 변경된 파일 정보를 저장합니다.
                renamed_files_info.append((original_file_path, new_file_path))
    return renamed_files_info

# Directory where the files are located
file_directory = "/home/gaeun/HV_plate/yolov5/plates.v7i.yolov5pytorch"

# Part to remove from the file names (including everything after it)
part_to_remove = "_bmp"

# Rename the files and remove the originals
renamed_files_info = rename_and_clean_files(file_directory, part_to_remove)

# Output the results
for old_path, new_path in renamed_files_info:
    print(f"Renamed '{os.path.basename(old_path)}' to '{os.path.basename(new_path)}'")
