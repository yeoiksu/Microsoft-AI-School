import numpy as np
arr1 = np.arange(0,10)
arr2 = arr1
arr3 = arr1.copy()
arr2[0] = 99
print("array1: ", arr1)  # arr1도 변경
print("array3: ", arr3)  # arr3은 그대로

# numpy 중복된 원소 제거
array = np.array([1, 2, 1, 2, 3, 4, 3, 4, 5])
print("중복 처리 전: ", array)
# 중복 처리 전 >>  [1 2 1 2 3 4 3 4 5]
print("중복 처리 후: ", np.unique(array))


# np.isin() -> 내가 찾는게 있는지 여부 각 index 위치에 true false
array = np.array([1, 2, 3, 4, 5, 6, 7])

iwantit = np.array([1, 2, 3, 10])

print(np.isin(array, iwantit))
# [ True  True  True False False False False]
