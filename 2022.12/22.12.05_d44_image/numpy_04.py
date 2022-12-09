import numpy as np
array = np.array([[5,2,7,6], [2,3,10,15]])
print("각 열을 기준으로 정렬 전\n", array)

array.sort(axis=0)  # 0:열, 1:행
print("각 열을 기준으로 정렬 후\n", array)