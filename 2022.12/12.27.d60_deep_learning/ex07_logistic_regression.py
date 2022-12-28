import numpy as np
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.linear_model import LogisticRegression

# iris data
iris = datasets.load_iris()
list_iris = []
# print(iris["data"])

# dict keys 무언인지 체크 필요
list_iris = iris.keys()
print(list_iris)
"""
dict_keys(['data', 'target', 'frame', 'target_names', 
'DESCR', 'feature_names', 'filename', 'data_module'])
"""
x = iris["data"][:, 3:]  # 꽃잎의 너비 변수 사용
print(iris["target_names"]) # ['setosa' 'versicolor' 'virginica']
y = (iris["target"]==2).astype("int") # ris-versinica: 1 아니면 0

log_reg = LogisticRegression(solver= "liblinear")
# 사이킷런의 LogisticRegression은 클래스 레이블을 반환하는 method : predict() 
# 클래스에 속할 확률을 반환하는 method : predict_proba()
# predict() : 확률 추정식에서 0보다 클 때는 "양성"으로 판단
# predict_proba() : 시그널
log_reg.fit(x,y)

# 이제 꽃잎이 너비가 0 ~3cm 꽃에 대해 모델으 ㅣ추정확률을 계산
x_new = np.linspace(0, 3, 1000).reshape(-1, 1)

# -1의 의미는 변경된 배열의 -1 위치의 차원은 원래 배열의 길이와 남은 
y_proba = log_reg.predict_proba(x_new)

# plt.plot(x_new, y_proba[:, 1], 'g-', label= "iris-virginica")      # 음성
# plt.plot(x_new, y_proba[:, 0], 'b--', label= "Not iris-virginica") # 양성
# plt.legend()
# plt.show()

######################## 보기 좋게 표현 
decision_boundary = x_new[y_proba[:, 1] >= 0.5][0]

plt.figure(figsize=(8, 3))  # 그래프 사이즈
plt.plot(x[y == 0], y[y == 0], "bs")  # 음성 범주 pointing
plt.plot(x[y == 1], y[y == 1], "g^")  # 양성 범주 pointing

# 결정경계 표시
plt.plot([decision_boundary, decision_boundary], [-1, 2], "k:", linewidth=2)

# 추정확률 plotting
plt.plot(x_new, y_proba[:, 1], 'g-', label='Iris-Virginica')  # 음성
plt.plot(x_new, y_proba[:, 0], 'b--', label='Not Iris-Virginica')  # 양성

# 결정 경계 표시
plt.text(decision_boundary+0.02, 0.15, "Decision boundary",
         fontsize=10, color="k", ha="center")
plt.arrow(decision_boundary, 0.08, -0.3, 0,
          head_width=0.05, head_length=0.1, fc='b', ec='b')
plt.arrow(decision_boundary, 0.92, 0.3, 0,
          head_width=0.05, head_length=0.1, fc='g', ec='g')
plt.xlabel("petal width(cm)", fontsize=10)
plt.ylabel("probability", fontsize=14)
plt.legend(loc='center left', fontsize=10)
plt.axis([0, 3, -0.02, 1.02])
plt.show()

## test
test_data = log_reg.predict([[1.6], [1.48]])

# 
print()