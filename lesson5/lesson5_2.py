import random

def play_game(): #此為自定義功能變數(function)，不會被執行
    min = 1
    max = 100
    count = 0
    target = random.randint(min, max)
    print(target)
    print("===============猜數字遊戲=================:\n")
    while(True):
        count += 1
        keyin = int(input(f"猜數字範圍{min}~{max}: "))
        if(keyin >=min and keyin <= max):
            if(keyin == target):
                print(f"賓果!猜對了, 答案是:{target}")
                print(f"您猜了{count}次")
                break
            elif (keyin > target):
                max = keyin - 1
                print("再小一點")
            elif (keyin < target):
                min = keyin + 1
                print("再大一點")
            print("您已經猜了",count,"次\n")
        else:
            print("請輸入提示範圍內的數字")
            
    
    
def main():    #此為自定義功能變數(function)，不會被執行
    while(True):
        play_game()
        play_again = input("您還要玩嗎?(y,n)")
        if play_again == "n":
            break
        elif play_again <> "n":
    print("Game Over")
    

if __name__ == "__main__":  #name的功能為知道目前是哪個功能變數在執行 #程式掃描到if才開始執行
    n = 0  #n為全域變數，如果放在function下就會變成區域變數，只有該功能可以讀取
    main()
    