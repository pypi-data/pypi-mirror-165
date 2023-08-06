import os,random

a1=random.randint(10000000,99999999)

a1=hex(a1)

print("激活码:{}".format(a1))

a1=str(a1)

print('你的电脑已被停用')
print('将在60分内注销您的登录')

os.startfile('1.vbs')

a=input('请输入激活码启用你的电脑:')
while 1:
    if a!=a1:
        a=int(input('激活码错误，请重新输入:'))
    print('激活码正确，正在进入系统...')
    os.startfile('2.vbs')
    print('激活成功')
    print('正在重新记录您的登陆')
    os.startfile('2.bat')
    print('您不会被注销您的登录')
    break
