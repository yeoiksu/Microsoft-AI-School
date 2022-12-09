import numpy as np

# 단일 객체 저장 및 불러오기
array = np.arange(0, 10)
print(array)

# .npy 파일에다가 저장하기
np.save("./2022.12/12.05_d44_image/data/save.npy", array)

# 불러오기
result = np.load("./2022.12/12.05_d44_image/data/save.npy")
print("result: ", result)
