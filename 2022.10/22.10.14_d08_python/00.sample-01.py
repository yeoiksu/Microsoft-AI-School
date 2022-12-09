#  숫자 게임 맞추기
import random

randNum = random.randint(1,100)
game_count = 1
print(randNum)

while True:    
    try:    
        inputNum = int(input("1~100 사이의 숫자를 입력하세요: "))
    
        if inputNum > randNum:
            # print("입력하신 숫자는 랜덤 Number보다 큽니다")
            print("DOWN")
        elif inputNum < randNum:
            # print("입력하신 숫자는 랜덤 Number보다 작습니다")
            print("UP")
        else:
            # print("축하합니다. 시도하신 횟수는 {}입니다".format(game_count))
            print(f"축하합니다. 시도하신 횟수는 {game_count}입니다")
            break
        game_count += 1

    except Exception as e:
        print('에러의 원인은', e)
    