#module可以提供function, class和常數三個內容
from machine import Timer #第一個字大寫表示為class #這裡的machine是指pico
#timer = Timer(period=5000, mode=Timer.ONE_SHOT, callback=lambda t:print(1)) #lambda為匿名引述
#Timer.ONE_SHOT只執行一次，常數要用全大寫
#timer = Timer(period=1000, mode=Timer.PERIODIC, callback=lambda t:print("hello pico"))
#Timer.PERIODIC連續執行，常數要用全大寫

from machine import Timer #這裡的machine是指pico

def callback1123(y): #function的功能是用來結構化程式 #def就是定義功能變數

    global count     #global是讓全域使用
    count +=1
    if count > 5:
        y.deinit()   #清除初始化
        print("END")
    else:
        print("keep going")

def main():
    tim = Timer(period=1500, mode=Timer.PERIODIC, callback=callback1123)
    
if __name__=="__main__":
    count = 0
    main()
