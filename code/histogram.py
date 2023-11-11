import cv2
import numpy as np
import matplotlib.pyplot as plt

# 이미지를 불러옵니다.
image_path = '/home/gaeun/HV_plate/yolov5/example/13-54-14_000_bmp.rf.c547a2258a87b748487f763e8b88e48e.jpg'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # 이미지를 그레이스케일로 변환합니다.

# 이미지의 히스토그램을 계산합니다.
histogram = cv2.calcHist([image], [0], None, [256], [0, 256])

# 히스토그램 시각화
plt.plot(histogram)
plt.title('Histogram')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')
plt.show()

# 밝기 분포 분석 및 임계값 선택
# 이 부분에서 밝기 분포를 분석하고, 적절한 임계값을 선택하면 됩니다.
# 예를 들어, 밝기 분포 중심에서 임계값을 선택하려면 중심값을 계산하고 해당 값을 임계값으로 설정하면 됩니다.

# 중심값 계산 (예: 밝기 분포 중심값)
center_value = np.argmax(histogram)  # 가장 빈도가 높은 픽셀 값

# 임계값 설정 (예: 중심값)
threshold_value = center_value

# 이미지 이진화
binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)[1]

# 결과 이미지 시각화
plt.subplot(1, 2, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(binary_image, cmap='gray')
plt.title('Binary Image')
plt.axis('off')

plt.tight_layout()
plt.show()
