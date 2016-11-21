#_*_ coding:utf-8 _*_

import os
import sys
import time
import re


str1="C:\\Users\\yangliyun\\test9\\baofengshowsetup_baofeng.exe"
filename=os.path.basename(str1)
print(filename)
filename1=filename[17:]
print(filename1)
filename2=filename1[:-4]
print(filename2)