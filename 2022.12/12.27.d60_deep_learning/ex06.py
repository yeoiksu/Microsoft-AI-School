# 파이토치의 nn.Linear와 nn.Sigmoid로 로지스틱 회귀를 구현
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# train data -> Tensor
x_data = [[1,2], [2,3], [3,1], [4,3], [5,3], [6,2]]
y_data = [[0], [0], [0], [1], [1], [1]]

# tensor
x_train = torch.FloatTensor(x_data)
y_train = torch.FloatTensor(y_data)

class BinaryClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(2, 1)  # input 2 output 1
        self.sigmoid = nn.Sigmoid()

    def foward(self, x):
        return self.sigmoid(self.linear(x))

# 모델 호출
model = BinaryClassifier()
print(model)
"""
BinaryClassifier(
  (linear): Linear(in_features=2, out_features=1, bias=True)
  (sigmoid): Sigmoid()
)
"""

optimizer = optim.SGD(model.parameters(), lr =0.1, momentum= 0.9) # optimizer 설정
epochs = 1000 # epoch 설정

for epoch in range(epochs + 1):
    output = model(x_train)

    # loss
    loss= F.binary_cross_entropy(output, y_train)

    optimizer.zero_grad()  # gradient를 None으로 설정
    loss.backward()
    optimizer.step()  # 단일 optimization step을 수행하고 parameter 업데이트
