from sklearn import datasets
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

iris = datasets.load_iris()  # iris 데이터셋
features = iris.data
target = iris.target

print(target)
print(features)

# LAD 객체 만들고 실행하여 특성을 변환합니다.
lda = LinearDiscriminantAnalysis(n_components= 1)
features_lad = lda.fit(features, target).transform(features)

# print("원본 특성 개수 : ", features.shape[1])
# print("줄어든 특성 개수 : ", features_lad.shape[1])

## 설명된 분산 비율이 담긴 배열을 저장
lda_var_ratios = lda.explained_variance_ratio_
print(lda_var_ratios)

def select_n_components(var_ratio, goal_val: float) -> int:
    total_variances = 0.0   # 설명된 분산의 초기값을 지정
    n_components = 0        # 특성 개수의 초기값을 지정

    for explaines_variance in var_ratio:  # 각 특성의 성명된 분산을 순회 loop
        total_variances += explaines_variance  # 설명된 분산 값을 누적
        n_components += 1  # 성분 개수를 카운트
        if total_variances >= goal_val:  # 설명된 분산이 목표치에 도달하면 반복을 종료
            break

    return n_components  # 성분 개수를 반환

temp = select_n_components(lda_var_ratios, 0.95)
print("temp = ", temp)