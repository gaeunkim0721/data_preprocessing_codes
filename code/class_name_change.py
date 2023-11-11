import os

# ID를 문자열 레이블 이름으로 매핑
id_to_name = {
    0: 'defect',
    1: 'edge_in_small_hole',
    2: 'edge_scratch',
    3: 'hole_press',
    4: 'poke',
    5: 'scratch',
    6: 'small_hole_closed',
    7: 'surface_scratch',
    8: 'thin_press',
    9: 'undefined'
}

# 소스 디렉토리 경로를 정의합니다.
source_directory = '/home/gaeun/Downloads/resized_images'

# 모든 .txt 파일을 순회합니다.
for filename in os.listdir(source_directory):
    if filename.endswith('.txt'):
        filepath = os.path.join(source_directory, filename)
        with open(filepath, 'r') as file:
            lines = file.readlines()

        updated_lines = []  # 변경된 줄들을 저장할 리스트
        for line in lines:
            # 줄의 내용이 있는지 확인하고 숫자로 시작하는지 확인
            if line.strip() and line.strip().split()[0].isdigit():
                parts = line.strip().split()
                # 리스트에 최소한 한 개의 요소가 있는지 확인
                if len(parts) >= 1:
                    try:
                        class_id = int(parts[0])  # 클래스 ID를 정수로 변환
                        if class_id in id_to_name:
                            # 클래스 ID를 문자열 레이블 이름으로 매핑
                            parts[0] = id_to_name[class_id]
                        else:
                            # id_to_name에 없는 ID는 처리하지 않음
                            print(f"Unknown class ID: {class_id}")
                            continue
                        updated_lines.append(' '.join(parts))
                    except ValueError:
                        # parts[0]이 정수가 아니면 오류 메시지를 출력
                        print(f"Invalid class ID: {parts[0]}")
            else:
                # 숫자로 시작하지 않는 줄은 건너뜀
                print(f"Non-annotation text skipped: {line.strip()}")

        # 변경된 어노테이션을 파일에 씁니다.
        with open(filepath, 'w') as file:
            for updated_line in updated_lines:
                file.write(updated_line + '\n')




import os

# 문자열 레이블을 ID로 매핑
name_to_id = {
    'defect': 0,
    'edge_in_small_hole': 1,
    'edge_scratch': 2,
    'hole_press': 3,
    'poke': 4,
    'scratch': 5,
    'small_hole_closed': 6,
    'surface_scratch': 7,
    'thin_press': 8,
    'undefined': 9
}

# 소스 디렉토리 경로를 정의합니다.
source_directory = '/home/gaeun/Downloads/resized_images'

# 모든 .txt 파일을 순회합니다.
for filename in os.listdir(source_directory):
    if filename.endswith('.txt'):
        filepath = os.path.join(source_directory, filename)
        with open(filepath, 'r') as file:
            lines = file.readlines()

        updated_lines = []  # 변경된 줄들을 저장할 리스트
        for line in lines:
            # 줄의 내용이 있는지 확인
            if line.strip():
                parts = line.strip().split()
                # 리스트에 최소한 한 개의 요소가 있는지 확인
                if len(parts) >= 1:
                    label_name = parts[0]
                    if label_name in name_to_id:
                        # 문자열 레이블을 숫자 ID로 매핑
                        parts[0] = str(name_to_id[label_name])
                        updated_lines.append(' '.join(parts))
                    else:
                        # name_to_id에 없는 레이블은 처리하지 않음
                        print(f"Unknown label name: {label_name}")
                else:
                    # parts 리스트가 비어 있으면 오류 메시지를 출력
                    print("Empty line found in the file.")

        # 변경된 어노테이션을 파일에 씁니다.
        with open(filepath, 'w') as file:
            for updated_line in updated_lines:
                file.write(updated_line + '\n')
