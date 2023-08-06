#!/usr/bin/env
# coding=utf-8
import math,sys,gc
import xiugay as xiugou
import random,os
import calendar as cal
import random,hh
import time as t
import tujian
import datetime,pygame,webbrowser
from pygame.locals import *
from math import *
# import some modules
def CN_allthing(qwe):
    def fileeee(qwe):
        file_name=r'./'
        m1="▫"
        m2="▪"
        m3=0
        scale = 50
        start = t.perf_counter()
        
        def file_count(file_dir):
            """

            # file count
            
            """
            count = 0
            for root, dirs, files in os.walk(file_dir):
                count += len(files)
            return count
        def file_size(file_dir):
            """

            # file size

            """
            size = 0
            for root, dirs, files in os.walk(file_dir):
                for file in files:
                    size+=os.path.getsize(os.path.join(root, file))
            return size
        for i in range(scale + 1):
            m4=m3%2
            if m4==0:m5=m1+m2
            else :m5=m2+m1
            a = "█" * i
            b = "." * (scale - i)
            c = (i / scale) * 100
            dur = t.perf_counter() - start
            print("\r>> LOADING {:^3.0f}%[{}{}]{:.2f}s {}".format(c,a,b,dur,m5))
            
            m3+=1
            
        a12345=file_count(file_name)
        a09876=file_size(file_name)
        print()
        print()
        import this
        print()
        
        for root,dirs,files in os.walk("./"):
            print(root)
            print(dirs)
            print(files,'\n')
        print('本文件夹有',a12345,'个文件')
        print('本文件夹有',a09876,'个 B 大')
        print('本文件夹有',(a09876)/1024,'个 KB 大')
        print('本文件夹有',(a09876)/1024/1024,'个 MB 大')
        print('本文件夹有',(a09876)/1024/1024/1024,'个 GB 大')
        print('本文件夹有',(a09876)/1024/1024/1024/1024,'个 TB 大')
        del a12345,a09876,file_name,m1,m2,m3,m4,m5,i,scale,start,dur,a,b,c
        gc.collect()
        hh.Print()
        print('dingdong,开机成功')
    fileeee(1)
    mins=[0,0,0,0,0,0]
    u=list(range(10))
    for i in range(6):
        a=random.randint(0,9)
        a=u[a]
        mins[i]=a
    minss=str(mins[0])+\
           str(mins[1])+\
           str(mins[2])+\
           str(mins[3])+\
           str(mins[4])+\
           str(mins[5])
    print('此处是验证码',minss,end=" ")
    ea=input('亲输入验证码:')
    if minss=='114514':
        print('哼哼哼哈哈哈哈哈哈哈哈~~~~~~~~~~')
        ea=minss
    if ea=='114514' or ea=='1919810':
        ea=minss
        print('好吧,勉强让你过')
    while ea!=minss:
        print('验证码验证失败，请重试')
        for i in range(6):
            a=random.randint(0,9)
            a=u[a]
            mins[i]=a
        minss=str(mins[0])+\
               str(mins[1])+\
               str(mins[2])+\
               str(mins[3])+\
               str(mins[4])+\
               str(mins[5])
        if minss=='114514':print('哼哼哼哈哈哈哈哈哈哈哈~~~~~~~~~~')
        print('此处是验证码',minss,end=" ")
        ea=input('亲输入验证码:')
        if ea=='114514' or ea=='1919810':
            ea=minss
            print('好吧,勉强让你过')
    del mins,minss
    del a
    gc.collect()
    print('验证码验证成功')
    print('hallo,world =) ')
    
    m=input('请登录,此处写公共密码:')
    while m!=num1:
        print('登陆失败,请重试')
        m=input('请登录,此处写公共密码:')
    print('登陆成功')
    print('你好,用户')

    ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')

    while 1:
        f=input('1:返回,2:继续')
        if f=='1':
            print("Good bye!")
            ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
        elif f=='2':
            if ea=='1':
                x=input('请登录,此处写密码:')
                while x!=num2:
                    print('登陆失败,请重试')
                    f=input('1:返回,2:继续')
                    if f=='1':
                        print("Good bye!")
                        ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
                    elif f=='2':x=input('请登录,此处写密码:')
                    else:print('error')
                print('boss,您好')
                boss=1
                user=0
                worker=0
                roadman=0
                break
            if ea=='2':
                print('user,您好')
                boss=0
                user=1
                worker=0
                roadman=0
                break
            elif ea=='3':
                print(' worker,你好')
                boss=0
                user=0
                worker=1
                roadman=0
                break
            elif ea=='4':
                print('roadman,快去干活')
                boss=0
                user=0
                worker=0
                roadman=1
                break
            elif ea=='114514' or ea=='1919810':
                print('哼哼哈哈哈哈哈哈哈~~~~~~')
                print('怎么到处都是homo(恼)',end=" ")
                print('滚')
                ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
            else:
                print('error')
                ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
        else:
            print('error')
    
    while 1:
        print('宁干甚么')
        print('0:开始菜单')
        print("1:计算器,2:时间")
        print('3:日期排序,4:退出账号,5:彩蛋栏')
        if boss==1:print("6:演示,7:密码更改,8:学习王(未完成)")
        a=input('请输入:')
        if a=='0':
            print('未实装')
        if a=='1':
            while 1:
                f=input('1:返回,2:继续')
                if f=='1':
                    print("Good bye!")
                    break
                elif f=='2':
                    print('1:加,2:减,3:乘,4:除:')
                    print('5:乘方,6:平方根,7:素数:')
                    print('8:9*9乘法表,9:因式分解,10:π:')
                    print('11:解一元一次方程,12:解一元二次方程:')
                    m=input('干什么:')
                    def count(qwe):
                        n1=int(input('请输入一个数字'))
                        n2=int(input('请输入另一个数字'))
                    if m=='1':
                        count(1)
                        print(n1+n2)
                    elif m=='2':
                        count(1)
                        print(n1-n2)
                    elif m=='3':
                        count(1)
                        print(n1*n2)
                    elif m=='4':
                        counttt=input('1:除,2:除(取整),6:除(取余)')
                        count(1)
                        if counttt=='1':
                            print(n1/n2)
                        if counttt=='2':
                            print(n1//n2)
                        if counttt=='3':
                            print(n1%n2)
                    elif m=='5':
                        count(1)
                        n1=math.pow(n1,n2)
                        print(n1)
                    elif m=='6':
                        n1=int(input('请输入一个数字'))
                        n1=math.sqrt(n1)
                        print(n1)
                    elif m=='7':
                        p1=0
                        a=int(input('请输入范围(2<=a<=i):'))
                        b=int(input('请输入范围(i<=b):'))
                        for m in range(a,b+1):
                            if m>=2:
                                for i in range(2,m):
                                    if m%i==0:break
                                else:
                                    p1=p1+1
                                    print(m,"是素数")
                            else:print('error')
                        print("Good bye!")
                        print('有{0}个素数'.format(p1))
                        p1=0
                    elif m=='8':
                        for i in range(1, 10):
                            print( )
                            for j in range(1, i+1):
                                print('{0}*{1}+={2}'.format(i,j,i*j),end=" ")
                        print('')
                    elif m=='9':
                        print('请不要输入非负数或字符!')
                        n=int(input('请输入一个数字(因式分解):'))
                        print('{}='.format(n),end="")
                        if not isinstance(n,int) or n<=0:
                            print('请输入一个正确的数字!')
                            n=int(input('请输入一个数字(因式分解):'))
                            print('{}='.format(n),end="")
                        elif n in [1]:print('{0}'.format(n),end="")
                        while n not in [1]:
                            for index in range(2,n+1):
                                if n%index==0:
                                    n//=index
                                    if n==1:print(index,end="")
                                    else:print ('{0} *'.format(index),end=" ")
                                    break
                        print()
                    elif m=='10':
                        n=10000+4
                        p=2*10**n
                        a=p//3;p+=a
                        i=2
                        while a>0:
                            a=a*i//(i*2+1);i+=1
                            p+=a
                        p//=10000
                        with open('.\ikun\\pi.txt', "w", encoding="utf-8") as f1m1:f1m1.write(p)
                        os.startfile('.\ikun\\pi.txt')
                        print('已计算')
                        del n,p,a,i
                        gc.collect()
                    elif m=='11':
                        while 1:
                            print('ax+b=c')
                            a=float(input('a=   ,(a!=0)'))
                            if a==0:print('a不得等于0')
                            else:break
                        b=float(input('b=    '))
                        c=float(input('c=    '))
                        a114514=(c-b)/a
                        print('x=',a114514)
                    elif m=='12':
                        while 1:
                            while 1:
                                print('ax^2+bx+c=d')
                                a=float(input('a=   ,(a!=0)'))
                                if a==0:print('a不得等于0')
                                else:break
                            b=float(input('b=    '))
                            c=float(input('c=    '))
                            d=float(input('d=    '))
                            a1919810=((4*a*d)-(4*a*c)+((b)**2))
                            if a1919810<0:
                                print('error')
                            else:
                                a19198101=(-b+math.sqrt(a1919810))/(2*a)
                                a19198102=(-b-math.sqrt(a1919810))/(2*a)
                                print('x1=',a19198101)
                                print('x2=',a19198102)
                    else:
                        print('error')
                else:
                    print('error')
        elif a=='2':
            while 1:
                f=int(input('1:返回,2:继续'))
                if f==1:
                    print("Good bye!")
                    break
                elif f==2:
                    def get_month_days(year, month):
                        if month >12 or month <= 0:
                            return -1
                        if month == 2:
                            return 29 if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 else 28
                        if month in (4, 6, 9, 11):
                            return 30
                        else:
                            return 31
                    print(t.strftime("%Y-%m-%d %H:%M:%S",t.localtime(t.time())))
                    year=int(t.strftime("%Y"))
                    month=int(t.strftime('%m'))
                    print("本月{}天".format(get_month_days(year,month)))
                    cal1=cal.month(year,month)
                    print("以下输出{0}年{1}月份的日历:".format(year,month))
                    print(cal1)
                    day=int(t.strftime('%d'))
                    months = (0,31,59,90,120,151,181,212,243,273,304,334)
                    sum=months[month - 1]
                    sum+=day
                    leap=0
                    if year%4==0 or year%400==0:leap=1
                    if leap==1 and month>2:sum+=1
                    print ('它是第%d天'%sum)
                    leap=0
                else:print('error')
        elif a=='3':
            while 1:
                f=int(input('1:返回，2:继续'))
                if f==1:
                    print(" Good bye!")
                    break
                elif f==2:
                    year= int(float(input('年:')))
                    month=int(float(input('月:')))
                    day = int(float(input('日:')))
                    def get_month_days(year, month):
                        if month >12 or month <= 0:
                            return -1
                        if month == 2:
                            return 29 if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 else 28
                        if month in (4, 6, 9, 11):
                            return 30
                        else:
                            return 31
                    print("本月{}天".format(get_month_days(year,month)))
                    months= (0,31,59,90,120,151,181,212,243,273,304,334)
                    if 0<month<=12:sum=months[month - 1]
                    else:print('error')
                    if 0<day<=31:pass
                    else:print('error')
                    sum+=day
                    leap=0
                    if year%4==0 or year%400==0:leap=1
                    if leap==1 and month>2:sum+=1
                    print ('它是第%d天'%sum)
                    leap=0
                else :print('error')
        elif a=='4':
            ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
            while 1:
                f=input('1:返回,2:继续')
                if f=='1':
                    print("Good bye!")
                    ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
                elif f=='2':
                    if ea=='1':
                        x=input('请登录,此处写密码:')
                        while x!=num2:
                            print('登陆失败,请重试')
                            f=input('1:返回,2:继续')
                            if f=='1':
                                print("Good bye!")
                                ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
                            elif f=='2':x=input('请登录,此处写密码:')
                            else:print('error')
                        print('boss,您好')
                        boss=1
                        user=0
                        worker=0
                        roadman=0
                        break
                    if ea=='2':
                        print('user,您好')
                        boss=0
                        user=1
                        worker=0
                        roadman=0
                        break
                    elif ea=='3':
                        print(' worker,你好')
                        boss=0
                        user=0
                        worker=1
                        roadman=0
                        break
                    elif ea=='4':
                        print('roadman,快去干活')
                        boss=0
                        user=0
                        worker=0
                        roadman=1
                        break
                    elif ea=='114514' or ea=='1919810':
                        print('哼哼哈哈哈哈哈哈哈~~~~~~')
                        print('怎么到处都是homo(恼)')
                        print('滚！')
                        ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
                    else:
                        print('error')
                        ea=input('请您选择用户:1:boss,2:user,3:worker,4:roadman:')
                else:print('error')
        elif a=='5':
            while 1:
                f=input('1:返回,2:继续')
                if f=='1':
                    print("Good bye!")
                    break
                elif f=='2':
                    e793492=input('请输入彩蛋码:')
                    if e793492=='114514' or e793492=='1919810':
                        xiugou.chousile(1919810114514)
                    elif e793492=='你干嘛哎哟' or e793492=='鸡你太美':
                        xiugou.xiaoheizishibushixiangjinjianyu(718327289)
                    elif e793492=="我有一个大胆的想法":
                        print('')
                        print('幼逝你,幼役思,拷进点我砍砍。蛰也太刑勒吧。')
                        print('蛰么有判头的日子可逝可狱不可囚,斩新的生活就在阎前啊。')
                        print('我拷,监值了蛰个,太可拷勒。刑啊,牢万家了吧。')
                        print('太刑勒蛰个,可狱而不可囚的人才呐。')
                        print('蛰日子终于能幼点判头勒。')
                        print('真逝牢有所痒,牢有所依啊。')
                        print('')
                    elif e793492=="佩洛西" or e793492=='peiluoxi':
                        while 1:
                            if boss!=1:
                                if roadman==1:print('※你无权访问,你越界了！')
                                if worker==1:print('你有这个资格吗,滚去工作吧,请')
                                else :print('你没有足够的权限')
                            f=int(input('1:返回,2:继续'))
                            if f==1:
                                print("Good bye! boss =) ")
                                break
                            elif f==2:
                                print('佩罗西来送死咯')
                                print("游戏后把窗口(无响应时)关掉")
                                
                                with open('.\ikun\\gread.txt','r') as f4:
                                    mi2=f4.readline()
                                    mi2=int(float(mi2))
                                print("往期记录：{}".format(mi2))
                                # 正确10位长度的时间戳可精确到秒
                                start=t.time()
                                time_array_start=t.localtime(start)
                                othtime_start=t.strftime("%Y-%m-%d %H:%M:%S",time_array_start)


                                clock=pygame.time.Clock()
                                tnndweishenmebuhe=120
                                SCREEN=443
                                offset={pygame.K_LEFT:0,pygame.K_RIGHT:0,pygame.K_UP:0,pygame.K_DOWN:0}
                                pygame.init()
                                screen = pygame.display.set_mode([SCREEN,SCREEN])
                                pygame.display.set_caption('python window')
                                background=pygame.image.load('.\ikun\\tnnd.jpg')
                                airplane=pygame.image.load('.\ikun\\pei.png')
                                peillllllll=pygame.image.load('.\ikun\\StartIcon.png')
                                gameover=pygame.image.load('.\ikun\\t0.jpg')
                                xiluo_pei=[0,443]
                                while 1:
                                    a1=14
                                    peiluoxi=[xiluo_pei[0]+a1,xiluo_pei[1]+a1]
                                    clock.tick(tnndweishenmebuhe)
                                    screen.blit(background,(0,0))
                                    screen.blit(airplane,xiluo_pei)
                                    screen.blit(peillllllll,peiluoxi)
                                    pygame.display.update()
                                    for event in pygame.event.get():
                                        if event.type==pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                        if event.type==pygame.KEYDOWN:
                                            if event.key in offset:
                                                offset[event.key]=3
                                        elif event.type==pygame.KEYUP:
                                            if event.key in offset:
                                                offset[event.key]=0
                                    xingcheng_x=xiluo_pei[0]+offset[pygame.K_RIGHT]-offset[pygame.K_LEFT]
                                    xingcheng_y=xiluo_pei[1]+offset[pygame.K_DOWN]-offset[pygame.K_UP]
                                    if xingcheng_x<=0:
                                        xiluo_pei[0]=0
                                    elif xingcheng_x>=SCREEN-52:
                                        xiluo_pei[0]=SCREEN-52
                                    else:
                                        xiluo_pei[0]=xingcheng_x
                                    if xingcheng_y<0:
                                        xiluo_pei[1]=0
                                    elif xingcheng_y>=SCREEN-52:
                                        xiluo_pei[1]=SCREEN-52
                                    else:
                                        xiluo_pei[1]=xingcheng_y
                                    peiluox=[peiluoxi[0]+a1-2,peiluoxi[1]+a1-2]
                                    if peiluox==[345,26] or peiluox==[346,26]:
                                        screen.blit(gameover,(0,0))
                                        break
                                            
                                end = t.time()
                                time_array_end=t.localtime(end)
                                othtime_end = t.strftime("%Y-%m-%d %H:%M:%S",time_array_end)
                                print(othtime_start,othtime_end)

                                link_start = datetime.datetime.strptime(othtime_start, '%Y-%m-%d %H:%M:%S')
                                link_end = datetime.datetime.strptime(othtime_end, '%Y-%m-%d %H:%M:%S')

                                mi=round((link_end - link_start).seconds / 60, 2)
                                mi=int(float(mi))
                                mi=(mi)*60
                                print('您用了',mi,'秒',sep='')
                                print('您用了',(mi)/60,'分钟',sep='')



                                if mi <= mi2:
                                    print("您破纪录了耶")
                                    mi=str(mi)
                                    with open('.\ikun\\gread.txt', "w", encoding="utf-8") as f3:f3.write(mi)
                                else :
                                    print('您没有破纪录哟')
                                    
                            else:print('error')
        elif a=='6':
            while 1:
                if boss!=1:
                    if roadman==1:print('※你无权访问,你越界了！')
                    if worker==1:print('你有这个资格吗,滚去工作吧,请')
                    if user==1:print('你没有足够的权限')
                f=int(input('1:返回,2:继续'))
                if f==1:
                    print("Good bye! boss =) ")
                    break
                elif f==2:
                    a=input('1:普通演示,2:权限演示')
                    if a=='1':
                        while 1:
                            f=input('1:返回,2:继续')
                            if f=='1':
                                print("Good bye!")
                                break
                            elif f=='2':print('404 Not Found')
                            else:print('error')
                    elif a=='2':
                        while 1:
                            if boss!=1:
                                if roadman==1:print('※你无权访问,你越界了！')
                                if worker==1:print('你有这个资格吗,滚去工作吧,请')
                                if user==1:print('你没有足够的权限')
                            f=int(input('1:返回,2:继续'))
                            if f==1:
                                print("Good bye! boss =) ")
                                break
                            elif f==2:print('404 Not Found')
                            else:print('error')
                else:print('error')
        elif a=='7':
            while 1:
                if boss!=1:
                    if roadman==1:print('※你无权访问,你越界了！')
                    if worker==1:print('你有这个资格吗,滚去工作吧,请')
                    if user==1:print('你没有足够的权限')
                f=int(input('1:返回,2:继续'))
                if f==1:
                    print("Good bye! boss =) ")
                    break
                elif f==2:
                    num10=input('boss,请输入原始密码:')
                    if num10!=num2:
                        print('密码错误')
                        num10=input('boss,请输入原始密码:')
                    num2=input('请输入新密码:')
                    xiugou.xiugay(553717805371)
                    with open('.\ikun\\num2.txt','w') as f2:f2.write(num2)                    
                    print('boss您的新密码是{0}'.format(num2))
                else:print('error')
        elif a=='8':
            while 1:
                if boss!=1:
                    if roadman==1:print('※你无权访问,你越界了！')
                    if worker==1:print('你有这个资格吗,滚去工作吧,请')
                    else :print('你没有足够的权限')
                f=int(input('1:返回,2:继续'))
                if f==1:
                    print("Good bye! boss =) ")
                    break
                elif f==2:
                    while 1:
                        print('boss好')
                        print('1:对战 2:图鉴 3:不干了')
                        a=input('what do you want to do ?')
                        if a=='1':
                            list2=[['灵魂诘问','神'],
                                   ['冯@娟','神'],
                                   ['校霸','神'],
                                   ['圣人光环','神'],
                                   ['直尺量角板','工具'],
                                   ['直尺量角板','工具'],
                                   ['三角板们','工具'],
                                   ['三角板们','工具'],
                                   ['奋斗','心态'],
                                   ['摆烂','心态'],
                                   ['发烧','疾病'],
                                   ['感冒','疾病'],
                                   ['电摇小子','手牌'],
                                   ['一线三等角','手牌'],
                                   ['李华','手牌'],
                                   ['华强的电动車','手牌'],
                                   ['半角模型','手牌'],
                                   ['圆周率','手牌'],
                                   ['bilibili','环境'],
                                   ['后排靠窗靠空调','神'],
                                   ['天气好热','环境']]
                            list3=[0,1]
                            players=['大黄','舟舟']
                            random.shuffle(list2)
                            random.shuffle(list3)
                            random.shuffle(players)
                            player1='boss:李导'
                            player2=players[0]
                            mycard=[]
                            computercard=[]
                            print("积分数：{}".format(sincow))
                            if sincow>=14:
                                print("注：正常双方 HP 4000,大师 HP 8000,赢不赢回合后结算",end="")
                                print("您好牛,特供 地狱模式 双方 99990HP ")
                                ppp=input("1:正常模式,2:大师模式,3:地狱模式")
                                sincos=1
                            else:
                                print("注：正常双方 HP 4000,大师 HP 8000,赢不赢回合后结算")
                                ppp=input("1:正常模式,2:大师模式")
                                sincos=0
                            while 1:
                                if ppp=='1':
                                    print("OK 正常")
                                    player1HP=4000
                                    player2HP=4000
                                    break
                                elif ppp=='2':
                                    print("OK 大师")
                                    player1HP=8000
                                    player2HP=8000
                                    break
                                elif ppp=="3":
                                    if sincos==1:
                                        print("OK 地狱")
                                        player1HP=99990
                                        player2HP=99990
                                        break
                                    else:
                                        print("error")
                                else:
                                    print("error")
                            del ppp,sincos
                            gc.collect()
                            a=1
                            while 1:
                                def Geipai_4pai_Give_Player1(qwe):
                                    input("{}的时间,点Enter键继续".format(player1))
                                    mycard1=list2[0]
                                    mycard2=list2[1]
                                    mycard3=list2[2]
                                    mycard4=list2[3]
                                    del list2[0],list2[1],list2[2],list2[3]
                                    mycardnew=[mycard1,mycard2,mycard3,mycard4]
                                    mycard.extend(mycardnew)
                                    print(player1,'获得',mycardnew)
                                    print(player1,'有',(" ".join(str(i) for i in mycard)))
                                    print(player1,'有',len(mycard),'张牌')
                                    print(player1,'的回合')
                                    print(player1,'有',player1HP,"HP")
                                    print(player2,'有',player2HP,"HP")
                                    while 1:
                                        for i in range(len(mycard) + 1):
                                            if i==0:
                                                print("{},不出牌".format(i))
                                            else:
                                                print("{},出{}".format(i,mycard[i - 1]))
                                        The_pack=int(float(input("请选择：")))
                                        if The_pack>=0:
                                            if The_pack==0:
                                                print("OK,你不出牌")
                                                break
                                            elif The_pack<=len(mycard):
                                                while 1:
                                                    print("1:Yes,2:No")
                                                    The_main=input("您确定要出这张牌：{}？".format(mycard[The_pack - 1]))
                                                    if The_main=='1':
                                                        print("OK,你不出{}".format(mycard[The_pack - 1]))
                                                        break
                                                    elif The_main=='2':
                                                        print('OK,你出{}'.format(mycard[The_pack - 1]))
                                                        pass#牌起效果
                                                        del mycard[The_pack - 1]
                                                    else:print('error')
                                            else:print("error")    
                                        else:print(error)
                                def Geipai_4pai_Give_Player2(qwe):
                                    input("{}的时间,点Enter键继续".format(player2))
                                    computercard1=list2[0]
                                    computercard2=list2[1]
                                    computercard3=list2[2]
                                    computercard4=list2[3]
                                    del list2[0],list2[1],list2[2],list2[3]
                                    computercardnew=[computercard1,computercard2,computercard3,computercard4]
                                    computercard.extend(computercardnew)
                                    print(player2,'有',len(computercard),'张牌')
                                    print(player2,'的回合')
                                    print(player1,'有',player1HP,"HP")
                                    print(player2,'有',player2HP,"HP")
                                    while 1:
                                        for The_pack in range(len(computercard) + 1):
                                            if len(computercard)==0:
                                                print("{}不出牌".format(player2))
                                                break
                                            else :
                                                print('OK,{}出{}'.format(player2,computercard[The_pack-1]))
                                                pass#牌起效果
                                                del computercard[The_pack-1]
                                def Geipai_1pai_Give_Player1(qwe):
                                    input("{}的时间,点Enter键继续".format(player1))
                                    if len(list2)==0:
                                        print('{}无牌可用'.format(player1))
                                    else:
                                        mycard1=list2[0]
                                        del list2[0]
                                        mycardnew=[mycard1]
                                        mycard.extend(mycardnew)
                                        print(player1,'获得',mycardnew)
                                        print(player1,'有',(" ".join(str(i) for i in mycard)))
                                        print(player1,'有',len(mycard),'张牌')
                                        print(player1,'的回合')
                                        print(player1,'有',player1HP,"HP")
                                        print(player2,'有',player2HP,"HP")
                                        while 1:
                                            for i in range(len(mycard) + 1):
                                                if i==0:
                                                    print("{},不出牌".format(i))
                                                else:
                                                    print("{},出{}".format(i,mycard[i - 1]))
                                            The_pack=int(float(input("请选择：")))
                                            if The_pack>=0:
                                                if The_pack==0:
                                                    print("OK,你不出牌")
                                                    break
                                                elif The_pack<=len(mycard):
                                                    while 1:
                                                        print("1:Yes,2:No")
                                                        The_main=input("您确定要出这张牌：{}？".format(mycard[The_pack-1]))
                                                        if The_main=='1':
                                                            print("OK,你不出{}".format(mycard[The_pack-1]))
                                                            break
                                                        elif The_main=='2':
                                                            print('OK,你出{}'.format(mycard[The_pack-1]))
                                                            pass#牌起效果
                                                            del mycard[The_pack-1]
                                                        else:print('error')
                                                else:print("error")    
                                            else:print(error)#player1出手
                                def Geipai_1pai_Give_Player2(qwe):
                                    input("{}的时间,点Enter键继续".format(player2))
                                    if len(list2)==0:
                                        print('{}无牌可用'.format(player2))
                                    else:
                                        computercard1=list2[0]
                                        del list2[0]
                                        computercardnew=[computercard1]
                                        computercard.extend(computercardnew)
                                        print(player2,'有',len(computercard),'张牌')
                                        print(player2,'的回合')
                                        print(player1,'有',player1HP,"HP")
                                        print(player2,'有',player2HP,"HP")
                                        while 1:
                                            for The_pack in range(len(computercard) + 1):
                                                if len(computercard)==0:
                                                    print("{}不出牌".format(player2))
                                                    break
                                                else :
                                                    print('OK,{}出{}'.format(player2,computercard[The_pack-1]))
                                                    pass#牌起效果
                                                    del computercard[The_pack-1]#player2出手
                                if list3[0]==0:
                                    if a==1:
                                        a=a-1
                                        Geipai_4pai_Give_Player1(1)
                                        if player1HP <= 0:
                                            if player2HP <= 0:
                                                print("平局")
                                            else:
                                                print(player1,'输了')
                                                print(player2,'赢了')
                                                sincow-=1
                                                with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                                print("积分减1")
                                            break
                                        if player2HP <= 0:
                                            print(player2,'输了')
                                            print(player1,'赢了')
                                            sincow+=1
                                            with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                            print("积分加1")
                                            break

                                        Geipai_4pai_Give_Player2(1)
                                        
                                        if player1HP <= 0:
                                            if player2HP <= 0:
                                                print("平局")
                                            else:
                                                print(player1,'输了')
                                                print(player2,'赢了')
                                                sincow-=1
                                                with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                                print("积分减1")
                                            break
                                        if player2HP <= 0:
                                            print(player2,'输了')
                                            print(player1,'赢了')
                                            sincow+=1
                                            with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                            print("积分加1")
                                            break

                                    elif a==0:
                                        Geipai_1pai_Give_Player1(1)
                                        if player1HP <= 0:
                                            if player2HP <= 0:
                                                print("平局")
                                            else:
                                                print(player1,'输了')
                                                print(player2,'赢了')
                                                sincow-=1
                                                with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                                print("积分减1")
                                            break
                                        if player2HP <= 0:
                                            print(player2,'输了')
                                            print(player1,'赢了')
                                            sincow+=1
                                            with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                            print("积分加1")
                                            break

                                        Geipai_1pai_Give_Player2(qwe)
                                        if player1HP <= 0:
                                            if player2HP <= 0:
                                                print("平局")
                                            else:
                                                print(player1,'输了')
                                                print(player2,'赢了')
                                                sincow-=1
                                                with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                                print("积分减1")
                                            break
                                        if player2HP <= 0:
                                            print(player2,'输了')
                                            print(player1,'赢了')
                                            sincow+=1
                                            with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                            print("积分加1")
                                            break

                                else :
                                    if a==1:
                                        a=a-1
                                        Geipai_4pai_Give_Player2(1)
                                        if player1HP <= 0:
                                            if player2HP <= 0:
                                                print("平局")
                                            else:
                                                print(player1,'输了')
                                                print(player2,'赢了')
                                                sincow-=1
                                                with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                                print("积分减1")
                                            break
                                        if player2HP <= 0:
                                            print(player2,'输了')
                                            print(player1,'赢了')
                                            sincow+=1
                                            with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                            print("积分加1")
                                            break

                                        Geipai_4pai_Give_Player1(qwe)
                                        if player1HP <= 0:
                                            if player2HP <= 0:
                                                print("平局")
                                            else:
                                                print(player1,'输了')
                                                print(player2,'赢了')
                                                sincow-=1
                                                with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                                print("积分减1")
                                            break
                                        if player2HP <= 0:
                                            print(player2,'输了')
                                            print(player1,'赢了')
                                            sincow+=1
                                            with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                            print("积分加1")
                                            break

                                    else:
                                        Geipai_1pai_Give_Player2(1)
                                        if player1HP <= 0:
                                            if player2HP <= 0:
                                                print("平局")
                                            else:
                                                print(player1,'输了')
                                                print(player2,'赢了')
                                                sincow-=1
                                                with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                                print("积分减1")
                                            break
                                        if player2HP <= 0:
                                            print(player2,'输了')
                                            print(player1,'赢了')
                                            sincow+=1
                                            with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                            print("积分加1")
                                            break

                                        Geipai_1pai_Give_Player1(1)
                                        if player1HP <= 0:
                                            if player2HP <= 0:
                                                print("平局")
                                            else:
                                                print(player1,'输了')
                                                print(player2,'赢了')
                                                sincow-=1
                                                with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                                print("积分减1")
                                            break
                                        if player2HP <= 0:
                                            print(player2,'输了')
                                            print(player1,'赢了')
                                            sincow+=1
                                            with open('.\ikun\\sincow.txt', "w", encoding="utf-8") as f111:f111.write(sincow)
                                            print("积分加1")
                                            break


                            a114514=input('还打不打？ 1:yes 2:no')
                            if a114514=='1':
                                print('ok')
                            elif a114514=='2':
                                print('goodbye')
                                break
                            else:
                                print("error")
                        elif a=='2':
                            tujian.tujian(1)
                        elif a=='3':
                            break
                        else :print('error')
                else:print('error')
        else :
            print('error')
'''
以下是正文
'''
def lichenggong(qwe):
    
    '''

    # the main thing
    
    '''
    
    num1='114514'
    with open('.\ikun\\num2.txt','r') as f1:
        num2=f1.readline()# give "num2
    with open('.\ikun\\upgread.txt','r') as fp:
        upgread=fp.readline()
    with open('.\ikun\\sincow.txt','r') as fm:
        sincow=fm.readline()
        sincow=int(float(sincow))
    if upgread=='0':
        print()
        print('您是初次使用我们巨硬的产品 noodows (R才怪) 0.2.2.0(内部版本 0.9.0.10920 build) 无图像版')
        print("You're use noodows (no R) 0.2.2.0(0.9.0.10920 build) no Image by Bignesshard")
        print()
        print('设置语言')
        print('Setup language')
        while 1:
            lauguage=input('1:English(no part),2:简体中文,3:繁體中文(未實裝)')
            if lauguage=='1':
                print('no part')
            elif lauguage=='2':
                print('OK!')
                break
            elif lauguage=='3':
                print('未實裝')
            else:
                print('error')
        with open('.\ikun\\lauguage.txt', "w", encoding="utf-8") as fp1:
            fp1.write(lauguage)
        print('欢迎使用')
        print('Thank you for your support!')
        with open('.\ikun\\lauguage.txt', "r", encoding="utf-8") as fpp1:
            lauguage=fpp1.readline()
        if lauguage=='1':
            print('error')
        elif lauguage=='2':
            CN_allthing(1)
        elif lauguage=='3':
            print('error')
        else :
            print('error')
    else:
        with open('.\ikun\\lauguage.txt', "r", encoding="utf-8") as fpp1:
            lauguage=fpp1.readline()
        if lauguage=='1':
            print('Hallo!')
            print('error')
        elif lauguage=='2':
            print('你好')
            CN_allthing(1)
        elif lauguage=='3':
            print('你好')
            print('error')
        else :
            print('error')
    
