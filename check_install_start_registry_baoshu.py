#_*_ coding:utf-8 _*_
import os
import glob
import sys
import win_tools
import global_var
import database_tools
import time


def check_install_start_registry_baoshu(file):

    print("[--------------------Now is testing:%s-------------------]"%file)
    #如果程序正在运行，先杀掉
    win_tools.kill_BaoFengShow()
    # 删除计算机遗留的用户信息
    win_tools.delete_userinfo()
    # 安装渠道包
    win_tools.auto_install(file)
    #读取注册表
    channelid=win_tools.analyze_registry()
    #启动程序-登录：
    win_tools.start_program()
    #查看上报到数据库是否正确
    global uuid
    uuid = win_tools.get_uuid()
    if uuid=="":
        print("无法得到uuid，可能是因为网络原因导致风秀客户端无法登录...这将会导致无法正常报数")
    global select_result
    select_result=database_tools.ssh_select(uuid, channelid)
    time.sleep(3)
    database_tools.ssh_delete(uuid)









#遍历安装渠道包并启动程序检查注册表和报数
def loop_check_install_start_registry_baoshu(file_path):
    global uuid_error
    global database_error
    uuid_error=0
    database_error=0
    file_list=glob.glob(file_path+"\\*.exe")
    for file in file_list:
        uuid_database=check_install_start_registry_baoshu(file)

        if uuid=="":
            uuid_error+=1
        if select_result=="":
            database_error+=1


    #因为第一个安装包安装时数据库中是否有此uuid，所以上报数据有可能不准，需要重新验证第一个安装包的报数
    uuid_database2=check_install_start_registry_baoshu(file_list[0])
    if uuid=="":
            uuid_error+=1
    if select_result=="":
            database_error+=1


#loop_check_install_start_registry_baoshu("C:\\Users\\yangliyun\\test9")