#!/usr/bin/env python3
import logging
import paramiko
import os
from pathlib import Path
from paramiko import SSHClient
from mtlibs.sshClient import SshClient
from mtlibs.SSH import SSH
import logging
logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    user_name = "root"
    password = "feihuo321"
    host="localhost"
    port = 2222
    
    client = SshClient(host,port=port, password=password, user=user_name)
    connect_success = client.connect()
    if not connect_success:
        logger.debug(f"连接失败 {user_name}@{host}:{port}")
        
    # 范例：执行命令
    cmd = "ls -al /"
    output = client.exec_cmd(cmd)
    logger.info(f"输出 {output}")
    
    # # demo: 下载整个文件夹
    # remotefile, local_file = '/.dockerenv', '.tmp/dockerenv1'
    # client.sftp_get(remotefile, local_file)  # 下载文件    
    # client.sftp_get_dir("/root",".tmp/test1")
   
	
    # 上传文件测试
    remotedir = "/app2"
    client.exec_cmd(f"mkdir {remotedir}")
    localdir = os.path.join(os.getcwd(),"deploy/uploads")
    
    client.sftp_put_dir(localdir,remotedir)  # 上传文件夹
    
    # 释放资源
    client.close()
    
    
if __name__ == "__main__":
    main()
    