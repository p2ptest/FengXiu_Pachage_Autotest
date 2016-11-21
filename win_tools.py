#_*_ coding:utf-8 _*_
import os
import sys
import shutil
import time
import global_var
import getpass
import winreg
import re

#判断共享目录是否可用
def test_net(netdir):
    if_exist = os.path.exists(netdir)
    #print(if_exist)
    if if_exist:
        is_dir=os.path.isdir(netdir)
        if not is_dir:
            print("%s is not directory" % netdir)
            print(global_var.usage)
            sys.exit()


#判断本地目录是否存在，存在则copy文件，不存在则创建后copy文件
def test_localdir(localdir):
    if_exist = os.path.exists(localdir)
    #print(if_exist)
    if if_exist:
        is_dir=os.path.isdir(localdir)
        if not is_dir:
            print("%s is not directory" % localdir)
            print(global_var.usage)
            sys.exit()
    else:
        try:
            print("directory is not exist，create it!")
            os.mkdir(localdir)
            #return 0
        except OSError as oserr:
            print("create directory failed %s" % oserr)
           # return 1
            sys.exit()

# 将文件从局域网拷贝到本地
def copy_file(netdir,localdir):
    print("\n *************************copy files************************\n")

    file_list=os.listdir(netdir)
    for file in file_list:
        try:
            shutil.copy(netdir+"\\"+file,localdir)
        except Exception as err:
            print("copy file from netdir to local dir errors %s"  % err)
            sys.exit()
    print("copy files success!")
    time.sleep(2)

    '''
    copy_cmd = "copy %s %s" % (netdir,localdir)
    copy_result=os.system(copy_cmd)
    if copy_result==0:
        print("copy file success")
        time.sleep(2)
    else:
        print("copy file from netdir to local dir errors")
        sys.exit()
    '''

#查看暴风进程是否存在，存在的话则删除
def kill_BaoFengShow():
    find_cmd="tasklist|find /i \"BaoFengShow.exe\" >nul 2>nul"
    kil_cmd="taskkill.exe /F /IM BaoFengShow.exe >nul 2>nul"
    find_result=os.system(find_cmd)
    if find_result==0:
        os.system(kil_cmd)
        print("BaoFengShow.exe is running,terminate it!")
        time.sleep(1)
    #kill_cmd="tasklist|find /i \"BaoFengShow.exe\"&&taskkill.exe /F /IM BaoFengShow.exe >nul 2>nul"
    #find_result=os.system(kill_cmd)
    #print(find_result)


# 删除计算机遗留的用户名密码信息
def delete_userinfo():
    user_info_path=global_var.user_info_path
    if os.path.exists(user_info_path):
        print("**********************delete userinfo******************")
        print("delete path:%s" % user_info_path)
        try:
            shutil.rmtree(user_info_path)
            print("delete userinfo success")
        except OSError as err:
            print("delete userinfo failed %s " % err)
            sys.exit()

#自动安装风秀包
def auto_install(file):
    print("\n************************install package***********************\n")
    install_cmd ="start /wait %s /silent" % file
    install_result=os.system(install_cmd)
    if install_result==0:
        print("install success!")
        time.sleep(2)
    else:
        print("install failed")
        sys.exit()


#解析注册表channelID值
def analyze_registry():
    print("\n**************************read registry*************************\n")
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\BaoFengShow.exe")
        value,type = winreg.QueryValueEx(key,"ChannelID")
        global CHANNELID
        CHANNELID = value
        print("ChannelID=%s" % CHANNELID)
        time.sleep(2)
        return CHANNELID
    except WindowsError as winerr:
        print("read registry failed")

#启动风秀程序
def start_program():
    print("\n**********************start client program*********************\n")
    start_cmd="start C:\"\Program Files (x86)\"\暴风秀场\BaoFengShow.exe >nul 2>nul"
    start_result=os.system(start_cmd)
    if start_result==0:
        print("start client program success")
        time.sleep(20)
    else:
        print("start BaoFengShow.exe failed")
        sys.exit()


#在Info.log中查找游客UUID
def get_uuid():
    print("\n*************************get uuid**************************\n")
    log_file = global_var.log_path
    #print(log_file)
    try:
        input_file = open(log_file,"rt",encoding="utf-8")
        time.sleep(2)
    except IOError as ioerr:
        print("open Info.log to get uuid  failed %s" % ioerr)
        sys.exit()

    input_file_list = input_file.readlines()
    input_file_str = " ".join(input_file_list)

    pattern = re.compile(r'YK_.{36}')
    match = pattern.search(input_file_str)
    input_file.close()
    if match:
        uuid=match.group()
        print("uuid:%s" %uuid)
        time.sleep(2)
        return uuid
    else:
        return ""

#kill_BaoFengShow()