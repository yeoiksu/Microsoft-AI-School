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

model = nn.Sequential(
    nn.Linear(2,1),  # input dim: 2 / output dim: 1
    nn.Sigmoid()
)

print(model(x_train))
"""
tensor([[0.5710],
        [0.6323],
        [0.8761],
        [0.8613],
        [0.9219],
        [0.9706]], grad_fn=<SigmoidBackward0>)
"""

optimizer = optim.SGD(model.parameters(), lr= 0.1)
epochs = 1000
for epoch in range(epochs+1):
    output = model(x_train)  # 예측값

    # loss
    loss = F.binary_cross_entropy(output, y_train) #차이

    # loss H(x)  계산
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        prediction = output >= torch.FloatTensor([0.5])     # 예측값이 0.5 넘으면 True 간주
        correct_prediction = prediction.float() == y_train  # 실제값과 일치하면 True
        acc = correct_prediction.sum().item() / \
                        len(correct_prediction)             # 정확도 계싼
        print("Epoch: {:4d}/{} loss:{:.6f} acc: {:.2f}%".format(
            epoch, epochs, loss.item(), acc*100
        ))

print(model(x_train))
"""
tensor([[0.0320],
        [0.1606],
        [0.3110],
        [0.7786],
        [0.9378],
        [0.9796]], grad_fn=<SigmoidBackward0>)
"""