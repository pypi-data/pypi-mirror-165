import time

m1="▫"
m2="▪"

m3=0
scale = 50
start = time.perf_counter()
for i in range(scale + 1):
    m4=m3%2
    if m4==0:m5=m1+m2
    else :m5=m2+m1
    a = "█" * i
    b = "." * (scale - i)
    c = (i / scale) * 100
    dur = time.perf_counter() - start
    print("\r>> Downloading {:^3.0f}%[{}{}]{:.2f}s {}".format(c,a,b,dur,m5),end = "")
    time.sleep(0.1)
    m3+=1
print()
print("OK完成")
