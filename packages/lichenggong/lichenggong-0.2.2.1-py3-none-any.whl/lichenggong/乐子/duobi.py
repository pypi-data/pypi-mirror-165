import sys
import time as t
import pygame
import datetime
from math import *
print("游戏后把窗口关掉")
with open('.\ikun\\well_do_you_think_it_is_very_cool.txt','r') as fm4:
    mp2=fm4.readline()
mp2=int(float(mp2))
print("往期记录：{}s".format(mp2))
# 正确10位长度的时间戳可精确到秒
start=t.time()
time_array_start=t.localtime(start)
othtime_start=t.strftime("%Y-%m-%d %H:%M:%S",time_array_start)

pygame.init()
font1=pygame.font.SysFont('microsoftyaheimicrosoftyaheiui',23)
textcc=font1.render('o',True,(250,0,0))
screen=pygame.display.set_mode((800,700),0,32)
missile=pygame.image.load('./ikun//rect1.png').convert_alpha()
height=missile.get_height()
width=missile.get_width()
pygame.mouse.set_visible(0)
xz1,yz1=101,601
velocity=500
time1=1/1000
tnndweishenmebuhe=120
clock=pygame.time.Clock()
clock.tick(tnndweishenmebuhe)
A=()
B=()
C=()
a=0
pygame.display.set_caption('python window')
while 1:
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
    xzz,yzz=pygame.mouse.get_pos()
    XXX=(xzz,yzz)
    distance=sqrt(pow(xz1-xzz,2)+pow(yz1-yzz,2))
    section=velocity*time1
    sina=(yz1-yzz)/distance
    cosa=(xzz-xz1)/distance
    angle=atan2(yzz-yz1,xzz-xz1)
    fangle=degrees(angle)
    xz1,yz1=(xz1+section*cosa,yz1-section*sina)
    missiled=pygame.transform.rotate(missile,-(fangle))
    if 0<=-fangle<=90:
        A=(width*cosa+xz1-width,yz1-height/2)
        B=(A[0]+height*sina,A[1]+height*cosa)
        
    if 90<-fangle<=180:
        A=(xz1 - width, yz1 - height/2+height*(-cosa))
        B=(xz1 - width+height*sina, yz1 - height/2)
        
    if -90<=-fangle<0:
        A=(xz1 - width+missiled.get_width(), yz1 - height/2+missiled.get_height()-height*cosa)
        B=(A[0]+height*sina, yz1 - height/2+missiled.get_height())
        
    if -180<-fangle<0:
        A=(xz1-width-height*sina, yz1 - height/2+missiled.get_height())
        B=(xz1 - width,A[1]+height*cosa )
    C=((A[0] + B[0])/2,(A[1] + B[1])/2)
    D=(xz1-width+(xz1-C[0]),yz1-height/2+(yz1-C[1]))
    screen.fill((0,0,0))
    screen.blit(missiled,D)
    screen.blit(textcc,XXX)
    end = t.time()
    time_array_end=t.localtime(end)
    othtime_end = t.strftime("%Y-%m-%d %H:%M:%S",time_array_end)

    link_start = datetime.datetime.strptime(othtime_start, '%Y-%m-%d %H:%M:%S')
    link_end = datetime.datetime.strptime(othtime_end, '%Y-%m-%d %H:%M:%S')

    mi=round((link_end - link_start).seconds / 60, 2)
    mi=int(float(mi))
    if mi>=10:
        velocity=1000
        if a==0:
            print("加速了！！！")
            a=a+1
    if D==XXX:
        print("寄")
        break
    pygame.display.update()
    

print(othtime_start,othtime_end)
mi=(mi)*60
print('您存活了',mi,'秒')
print('您存活了',(mi)/60,'分钟')
if mi <= mp2:
    print("您破纪录了耶")
    mi=str(mi)
    with open('.\ikun\\hahhahahhah.txt', "w", encoding="utf-8") as f3:f3.write(mi)
else :
    print('您没有破纪录哟')
