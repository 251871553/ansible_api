#!/usr/bin/env  python
#coding:utf-8
import multiprocessing
import sys
import paramiko
#import warnings

#warnings.filterwarnings('ignore')

from MyMariadb_api import Mariadb_api

mymariadb=Mariadb_api()


def ssh(hostname, port, username, password, remote_cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname, port, username, password, timeout=5)
        # stdin, stdout, stderr = ssh.exec_command(remote_cmd,get_pty=True)
        stdin, stdout, stderr = ssh.exec_command(remote_cmd)
        #    stdin.write('app\n')
        #   stdin.flush()
        #result = stdout.read(), stderr.read()
        ssh.close()
        return (hostname, 0)
    except Exception as e:
        # print(hostname,e)
        # print e.args[0]
        connect_error = ''
        if e.args[0] == 'timed out':
            connect_error = 1
        elif e.args[0] == 'Authentication failed.':
            connect_error = 2
        elif e.args[0] == 'Bad authentication type':
            connect_error = 3
        else:
            connect_error = 4
            #print  hostname,e.args[0]
        # print  hostname,connect_error
        return (hostname, connect_error)


#select_sql = "SELECT ip,port,user,passwd FROM jiqi_all where ip='10.12.16.32';"
#select_sql = "SELECT ipaddr,sshport,sshuser,sshpasswd FROM jiqi_all where ipaddr='10.12.16.32' "
select_sql = "SELECT ipaddr,sshport,sshuser,sshpasswd FROM jiqi_all"
#select_sql = "SELECT ip,port,user,passwd  from jiqi_all where conn_code ='2';"
#select_sql = "SELECT ip,port,user,passwd FROM arp_compare;"
connect_info=mymariadb.select_db(select_sql)
print len(connect_info)
#sys.exit()

cmd='echo 0'

pool = multiprocessing.Pool(processes=50)
result = {}
for  i in  connect_info:
         # print i
          ipaddr=i[0]
          conn_port=int(i[1])
          username=i[2]
          password=i[3]
          #print  ipaddr,conn_port,username,password
          a=pool.apply_async(ssh, (ipaddr,conn_port,username, password,cmd, ))
          result[ipaddr]=a
pool.close()
pool.join()



#sys.exit()
number=0
for  k,v in result.items():
   #  print('\033[32m[%s]\033[0m'  %k)
     number=number+1
     print('number %s machine output:\n ' %number)
     result_list=v.get()
    # result_list=list(result_list)
     if result_list:
        conn_code=result_list[1]
        update_sql = "update jiqi_all set conn_code = '%s' where ipaddr='%s' ;" % (conn_code, result_list[0])
        #print update_sql
        mymariadb.update_db(update_sql)

