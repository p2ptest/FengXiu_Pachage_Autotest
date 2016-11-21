#_*_ coding:utf-8 _*_

import os
import glob
import sys
import win_tools
import global_var
import check_install_start_registry_baoshu
import database_tools
import time


#判断命令行的参数是否正确
if len(sys.argv) < 3:
    print(global_var.usage)
    sys.exit()
#判断网络资源是否可用
win_tools.test_net(sys.argv[1])
#判断本地目录是否存在，不存在则创建
win_tools.test_localdir(sys.argv[2])
#拷贝安装包到本地
win_tools.copy_file(sys.argv[1], sys.argv[2])


#check_install_start_registry_baoshu.loop_check_install_start_registry_baoshu(sys.argv[2])
def check_install_start_registry_baoshu(file):

    print("[--------------------Now is testing:%s-------------------]"%file)
    #如果程序正在运行，先杀掉
    win_tools.kill_BaoFengShow()
    # 删除计算机遗留的用户信息
    win_tools.delete_userinfo()
    # 安装渠道包
    win_tools.auto_install(file)
    #读取注册表
    global channelid
    channelid=win_tools.analyze_registry()

    #启动程序-登录：
    win_tools.start_program()
    #查看上报到数据库是否正确
    global uuid
    uuid = win_tools.get_uuid()
    if uuid=="":
        print("无法得到uuid，可能是因为网络原因导致风秀客户端无法登录...请检查网络")
    global select_result
    select_result=database_tools.ssh_select(uuid, channelid)
    time.sleep(3)
    database_tools.ssh_delete(uuid)

#遍历安装渠道包并启动程序检查注册表和报数
def loop_check_install_start_registry_baoshu(file_path):
    global uuid_error
    global database_error
    global channelid_error
    uuid_error=0
    database_error=0
    channelid_error=0
    file_list=glob.glob(file_path+"\\*.exe")
    for file in file_list:
        uuid_database=check_install_start_registry_baoshu(file)
        if uuid=="":
            uuid_error+=1
        if select_result=="":
            database_error+=1


        filename=os.path.basename(file)
        filename1=filename[17:]
        filename2=filename1[:-4]
        if  filename2.lower()!=channelid.lower():

            channelid_error+=1
    #因为第一个安装包安装时数据库中是否有此uuid，所以上报数据有可能不准，需要重新验证第一个安装包的报数
    uuid_database2=check_install_start_registry_baoshu(file_list[0])
    if uuid=="":
            uuid_error+=1
    if select_result=="":
            database_error+=1


if __name__ == "__main__":
    loop_check_install_start_registry_baoshu(sys.argv[2])
    print("\n\n****************finally result*******************\n\n")
    if uuid_error!=0:
        print("Failed")
        print("有%d次登录失败，可能是由于网络原因导致无法登录" % uuid_error)
    if database_error!=0:
        print("Failed")
        print("有%d报数失败，请查看是否和网络原因有关" % database_error)
    if channelid_error!=0:
        print("Failed")
        print("有%d次注册表渠道与安装包所属渠道不一致" %channelid_error)
    if uuid_error==0 and database_error==0 and channelid_error==0:
        print("Success")


