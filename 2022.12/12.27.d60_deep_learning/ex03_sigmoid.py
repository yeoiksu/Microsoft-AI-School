import numpy as np
import matplotlib.pyplot as plt

# [-10 ~ 10] 구간에서 100개의 값을 시그모이드 함수에 대입
t = np.linspace(-10, 10 ,100)

# 시그모이드 공식
# np.exp : 함수 및 base 이 자연상수 e인 지수함수로 변환
sig = 1 / (1+np.exp(-t))

# t와 시그모이드 결과
plt.figure(figsize= (9,3))
plt.plot([-10,10], [0,0], 'k-')     # y축 기준 0.5 실선 하나
plt.plot([-10,10], [0.5,0.5], 'k:') # y축 기준 1   실선 하나
plt.plot([-10,10], [1, 1], 'k:') # y축 기준 1   실선 하나
plt.plot([0, 0], [-1.1, 1.1], 'k-') # y축 기준 1   실선 하나
plt.plot(t, sig, 'r-', linewidth= 2, 
    label= r"$\sigma(t) = \frac{1}{1 + e^{-t}}$")
plt.xlabel("t")
plt.legend(loc= "upper left", fontsize= 20)
plt.axis([-10,10,-0.1,1.1])
plt.show()