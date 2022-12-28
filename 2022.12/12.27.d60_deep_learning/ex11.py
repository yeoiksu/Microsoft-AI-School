# 파이토치로 다층 퍼셉트론 구현
import torch
import torch.nn as nn

# gpu 사용가능 여부
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

# xor 문제를 풀기 위한 입력 과 출력 정의
x = [[0, 0], [0, 1], [1, 0], [1, 1]]
y = [[0], [1], [1], [0]]

x = torch.tensor(x, dtype=torch.float32).to(device)
y = torch.tensor(y, dtype=torch.float32).to(device)

# model
# 입력층/은닉층1/은닉층2/은닉층3/출력층
model = nn.Sequential(
    nn.Linear(2, 10, bias= True),  # input: 2 / hidden 1: 10 
    nn.Sigmoid(),
    nn.Linear(10, 10, bias= True), # hidden 1: 10 / hidden 2: 10
    nn.Sigmoid(),
    nn.Linear(10, 10, bias= True), # hidden 2: 10 / hidden 3: 10
    nn.Sigmoid(),
    nn.Linear(10, 1, bias= True),  # hidden 3: 10 / out : 1
    nn.Sigmoid()  # Loss BCELoss 이므로 마지막 레이어를 sigmoid 사용 
).to(device)

criterion = torch.nn.BCELoss().to(device)
optimizer = torch.optim.SGD(model.parameters(), lr = 0.1)
epochs = 40000
for epoch in range(epochs+1):
    output = model(x)

    loss = criterion(output, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print(f"Epoch : {epoch} Loss : {loss.item()}")

# 인퍼런스 코드
with torch.no_grad():
    output = model(x)
    predicted = (output >0.5).float()
    acc = (predicted ==y).float().mean()
    
    print("모델의 출력값 output: ", output.detach().cpu().numpy())
    print("모델의 예측값 output: ", predicted.detach().cpu().numpy())
    print("실제값 (Y) ", y.cpu().numpy())
    print("정확도 -> ", acc.item())



