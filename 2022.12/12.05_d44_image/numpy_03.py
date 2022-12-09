# Numpy
import numpy as np

# 1. 원소정렬
array = np.array([15,20,5,12,7])
np.save("./2022.12/12.05_d44_image/data/array.npy", array)  # .npy 파일에다가 저장

array_data = np.load("./2022.12/12.05_d44_image/data/array.npy")  # 불러오기
array_data.sort()  # 오름차순
print("오름차순: ", array_data)
print("내림차순: ", array_data[::-1])  # 내림차순