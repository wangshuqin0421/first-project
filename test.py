#coding=utf-8                 
from P4 import P4,P4Exception  
import os, sys
import tarfile
from ftplib import FTP
import time

p4 = P4()                        
p4.port = "10.21.122.9:1666"
p4.user = "shuqin.wang"
p4.client = "shuqin.wang_O1PCCB07072082_2961"           
p4.password='FNb5jKAFf'
p4.charset = "utf8"
p4.connect()     
p4.run_login()

file_local_path = p4.run_where(sys.argv[1])[0]['path']#go文件在本地的路径|r'//TestDepot/Golang'
try:
    os.chdir(file_local_path)#切换工作路径
    os.popen('go build','r',1)#os.popen()方法执行终端命令'go build'编译获得新的二进制文件
except Exception as err:
    print(err)#打印出异常信息
    exit()#中断脚本

gofile_local_path = p4.run_where(sys.argv[2])[0]['path'] + '.exe'#编译过后的文件的路径|r'//TestDepot/Golang/hello'
data_local_path = p4.run_where(sys.argv[3])[0]['path']#data文件夹在本地的路径|r'//TestDepot/Golang/data'
#将data目录下面的文件和编译后的文件一起打包+压缩到"server_package_打包时的时间戳.tar.gz"
file_name = ('\server_package_'+str(time.time()))#带时间戳的文件名  
#指定压缩文件生成的文件夹的路径|r'C:\Users\shuqin.wang\Perforce\shuqin.wang_O1PCCB07072082_2961\wsq'
tar_file_path = sys.argv[4]+ file_name + '.tar.gz'#生成的文件路径
tar_file = tarfile.open(tar_file_path,'w:gz',encoding = 'utf-8')#创建压缩文件
tar_file.add(gofile_local_path)#添加要压缩的内容
tar_file.add(data_local_path)
tar_file.close()

#连接到ftp服务器
ftp_server = FTP()
ftp_server.connect('10.21.122.13')
ftp_server.login('release','zkehJMtkJ')

folder_name = 'server'
if folder_name in ftp_server.nlst():#检查server文件夹是否存在
    ftp_server.cwd(folder_name)#切换至server目录下
    ftp_server.storbinary(f'STOR {os.path.split(tar_file_path)[1]}', open(tar_file_path, 'rb'))#存在的话直接上传
else:
    ftp_server.mkd(folder_name)#创建server目录
    ftp_server.cwd(folder_name)
    ftp_server.storbinary(f'STOR {os.path.split(tar_file_path)[1]}', open(tar_file_path, 'rb'))
print(ftp_server.dir())#可以看到在server目录下成功上传的文件
ftp_server.quit()
p4.disconnect()
