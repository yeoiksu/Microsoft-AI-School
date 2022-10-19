#  내 ip주소 가져오기
import socket

# gethostbyname: 이름으로 ip주소 가져오기
# gethostname  : 이름을 가져오기
inAddr = socket.gethostbyname(socket.gethostname())
print(inAddr)

