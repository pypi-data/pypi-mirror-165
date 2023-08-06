import psutil
import platform
def a1(a):
    PlATFORM = platform.system()
    print("当前环境：",end="")
    if PlATFORM == "Linux":
        print('linux')
    elif PlATFORM == "Windows":
        print('Windows')
    elif PlATFORM == "Mac":
        print('Mac')
    else:
        print('其他') 

def get_disk_info():
    # 循环磁盘分区
    for disk in psutil.disk_partitions():
        # 读写方式 光盘 or 有效磁盘类型
        if 'cdrom' in disk.opts or disk.fstype == '':continue
        disk_name_arr = disk.device.split(':')
        disk_name = disk_name_arr[0]
        disk_info = psutil.disk_usage(disk.device)
        # 磁盘剩余空间，单位GB
        free_disk_size = disk_info.free//1024//1024//1024
        # 当前磁盘使用率和剩余空间G信息
        info="{}盘使用率：{}%,剩余空间：{}GB    ".format(disk_name, str(disk_info.percent), free_disk_size)
        print(info)
# cpu信息
def get_cpu_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_info = "CPU使用率：%i%%" % cpu_percent
    print(cpu_info)
# 内存信息
def get_memory_info():
    virtual_memory = psutil.virtual_memory()
    used_memory = virtual_memory.used/1024/1024/1024
    free_memory = virtual_memory.free/1024/1024/1024
    memory_percent = virtual_memory.percent
    memory_info = "内存使用：%0.2fG,使用率%0.1f%%,剩余内存：%0.2fG" %(used_memory, memory_percent, free_memory)
    print(memory_info)
if __name__ == '__main__':
    a1(1)
    get_disk_info()
    get_cpu_info()
    get_memory_info()
