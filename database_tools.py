import paramiko
import time
import re
#ssh 远程服务器并查询数据库中用户uuid信息
def ssh_select(uuid,channel):
    print("\n************************read database****************************\n")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("123.206.52.240",9604,"root","Password123@!@#",timeout=5)
        cmd1 = "ssh root@10.141.78.27 -p 9508"
        stdin,stdout,stderr = ssh.exec_command(cmd1)
        stdin.write("Password123@!@#")
        cmd = "cd /home/yangliyun;./BD_sql_select.sh   "+uuid
        stdin,stdout,stderr = ssh.exec_command(cmd)
        out_list = stdout.readlines()
        #print(out_list)
        out_str = ';'.join(out_list)
        print(out_str)

        pattern = re.compile(r'pak_ver:*.*.*.*,')
        match = pattern.search(out_str)

        if channel in out_str and match:
            print("t_usr_channel: bao shu success")
            print("t_big_Monitor:bao shu success")
        else:
            print("bao shu failed")
        ssh.close()
        print("\n")

        time.sleep(3)
        return match.group()
    except :
        print("select database Eror")
        return ""

#ssh 远程服务器并删除数据库中用户uuid信息
def ssh_delete(uuid):
    print("\n*****************delete database where uuid is my uuid******************\n")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("123.206.52.240",9604,"root","Password123@!@#",timeout=5)
        cmd1 = "ssh root@10.141.78.27 -p 9508"
        stdin,stdout,stderr = ssh.exec_command(cmd1)
        stdin.write("Password123@!@#")
        cmd = "cd /home/yangliyun;./BD_sql_delete.sh   "+uuid
        stdin,stdout,stderr = ssh.exec_command(cmd)
        out_list = stdout.readlines()
        #print(out_list)
        out_str = ';'.join(out_list)
        print(out_str)
        ssh.close()
        print("delete success\n")
        print("*******************************************************")
        print("\n\n\n")
        time.sleep(2)
    except :
        print("delete database error")



