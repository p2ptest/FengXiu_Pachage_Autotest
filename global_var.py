import os
import getpass

#获取计算机用户名信息
username = getpass.getuser()

log_path="C:\\Users\\"+username+"\\AppData\\Roaming\\fengxiu\\BaoFengShow\\Log\\Unity\\Info.log"
user_info_path="C:\\Users\\"+username+"\\AppData\\LocalLow\\FengXiu"

usage = "\n usage:main.py network-directory  localdirectory \n for example: main.py \\\\192.168.200.22\\publish\暴风影音\\11-风秀\\1-安装包\\fengxiu-201611091125  C:\\Users\\yangliyun\\test29"

