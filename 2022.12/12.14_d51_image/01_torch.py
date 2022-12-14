import torch
import numpy as np

data = [[1,2], [3,4]]
x_data = torch.tensor(data)
# print(x_data, '\n')
# print(x_data.shape, '\n')

# numpy 배열
x_ones = torch.ones_like(x_data)
# print(f"Ones Tensor >>\n", x_ones, '\n')

x_rand = torch.rand_like(x_data, dtype= torch.float)
# print(x_rand, '\n')

# shape = (3, 3)
# randn_tensor = torch.rand(shape)
# ones_tensor  = torch.ones(shape)
# zeros_tensor = torch.zeros(shape)

# print(f"Random Tensor >>\n", randn_tensor, '\n')
# print(f"Ones Tensor >>\n"  , ones_tensor , '\n')
# print(f"Zeros Tensor >>\n" , zeros_tensor, '\n')

tensor = torch.rand(3, 4)
# print(f"Shape of tensor: {tensor.shape}")
# print(f"Data type of tensor: {tensor.dtype}")
# print(f"Device tensor is stored on : {tensor.device}", '\n')

if torch.cuda.is_available():
    tensor = tensor.to('cuda')
else:
    tensor = tensor.to('cpu')
# print("Device tensor is stored on : ", tensor.device)

tensor  = torch.ones((4,4))
# tensor[: , 1] = 3
# print(tensor)

# 텐서 합치기
# t1 = torch.cat([tensor, tensor, tensor], dim = 1)
# t2 = tensor * tensor
# print(t1, '\n')
# print(t2)

# t  = torch.ones(5)
# t.add_(5)
# n = t.numpy
# print(t)
# print(n)

# n = np.ones(5)
# t = torch.from_numpy(n)
# print(n)
# print(t)

# np.add(n, 1, out = n)
# print(n)
# print(t)

# view
t = np.array( [[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]] )
ft = torch.FloatTensor(t)
# print(ft.shape)
# print(ft)

# # 3차원 텐서 변경
# print(ft.view([-1,1,3]))
# print(ft.view([-1,1,3]).shape)

# 스퀴즈 : 1인 차원 제거
# 3 x 1
ft = torch.FloatTensor([[0], [1], [2]])
# print(ft)
# print(ft.shape)

# print(ft.squeeze())
# print(ft.squeeze().shape)

# 언스퀴즈
# print(ft.unsqueeze(0))
# print(ft.unsqueeze(0).shape)