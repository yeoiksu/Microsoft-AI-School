import numpy as np
# 실행마다 결과 동일
# 랜덥값이 실행될때마다 변경되지않도록 seed 값 설정
np.random.seed(5)
print(np.random.randint(0,10,(2,3)))  # (2,3) 행렬, 0~10 값 랜덤