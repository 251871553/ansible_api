#!/usr/bin/env  python
#coding:utf-8

import paramiko
import multiprocessing
import sys
import warnings
from MyMariadb_api import Mariadb_api

mymariadb=Mariadb_api()


warnings.filterwarnings('ignore')


def  ssh(hostname,port,username,password,remote_cmd):
       ssh = paramiko.SSHClient()
       ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       try:
          ssh.connect(hostname,port,username, password,timeout=5)
      # stdin, stdout, stderr = ssh.exec_command(remote_cmd,get_pty=True)
          stdin, stdout, stderr = ssh.exec_command(remote_cmd)
   #    stdin.write('app\n')
    #   stdin.flush()
          result = stdout.read(),stderr.read()
          ssh.close()
          return result
       except Exception, e:
          return []

#select_sql = "SELECT ipaddr,sshport,sshuser,sshpasswd  from jiqi_all where conn_code ='0';"
#select_sql = "SELECT ipaddr,sshport,sshuser,sshpasswd  from jiqi_all where conn_code ='0' and   dns_list='10.12.43.12' ;"
select_sql = "SELECT ipaddr,sshport,sshuser,sshpasswd  from jiqi_all where conn_code ='0' and  dns_list  LIKE '%114.114.114.114%' ;"
#select_sql = "SELECT ip,port,user,passwd  from jiqi_all where conn_code ='0' and id <=50 ;"
#select_sql = "SELECT ip,port,user,passwd  from jiqi_all where conn_code ='0' and id >=100 and id <=500;"
#select_sql = "SELECT ip,port,user,passwd  from jiqi_all where ip ='10.11.12.15';"
connect_info=mymariadb.select_db(select_sql)
print len(connect_info)
#sys.exit()

#cmd='source   /etc/profile;tar  zxf /tmp/agent-20190325.tar.gz  -C  ~/ ; ~/agent/python3/bin/python ~/agent/agent_tasks.py start'
#cmd='pwd'
#cmd=r"source   /etc/profile;cat  /service/scripts/public/ipset.sh |  grep  'ipset -A baozun_ops 10.11.6.0/24' |  grep  -v  grep  || sed  -i '/ipset -N baozun_ops iphash/a\ipset -A baozun_ops 10.11.6.0/24'  /service/scripts/public/ipset.sh"
#cmd='source /etc/profile;sudo iptables -A INPUT -m set --match-set baozun_ops src -p tcp --dport 4489 -j ACCEPT'
#cmd="echo '%s' | sudo  -S netstat -anpt  |  grep  80 | grep  -v  '127.0.0.1'  | grep -v 'grep' "  % (password,i)
#cmd="echo '%s' | sudo  -S sed    s#8.8.8.8#10.12.43.12#g  /etc/resolv.conf  "  % (password,i)
#cmd='source /etc/profile;sh /tmp/22.sh'
#cmd='ps  aux  | grep  postgre'

pool = multiprocessing.Pool(processes=16)
result = {}
for  i in  connect_info:
         # print i
          ipaddr=i[0]
          conn_port=int(i[1])
          username=i[2]
          password=i[3]
         # cmd='source /etc/profile;cat /etc/resolv.conf | grep ^nameserver  ' 
#          cmd='source /etc/profile;sh /tmp/22.sh %s > /tmp/33.log ; cat  /tmp/33.log  '  % ipaddr
         # cmd="echo '%s' | sudo  -S netstat -anpt  |  grep  80 | grep  -v  '127.0.0.1'  | grep -v 'grep' "  % password
          cmd="echo '%s' | sudo  -S sed -i   s#114.114.114.114#10.12.43.11#g  /etc/resolv.conf  "  % password
         # cmd="echo '%s' | sudo  -S sed -i   s#8.8.8.8#10.12.43.12#g  /etc/resolv.conf  "  % password
#          cmd="echo '%s' | sudo  -S sed -i   s#10.12.43.12#10.12.43.11#g  /etc/resolv.conf  "  % password
          #cmd="echo '%s' | sudo  -S cat  /etc/resolv.conf | grep ^nameserver  | grep  '10.12.43.12'  ||  echo 'nameserver 10.12.43.12' >> /etc/resolv.conf  "  % password
#          cmd="echo '%s' | sudo  -S  echo 'nameserver 10.12.43.12' | sudo tee -a /etc/resolv.conf "  % password
          #cmd="echo '%s' | sudo  -S  echo 'nameserver 10.12.43.11' | sudo tee  /etc/resolv.conf "  % password
          #cmd="echo '%s' | sudo  -S cat  /etc/resolv.conf | grep ^nameserver  | grep  '10.12.43.11'  ||  echo 'nameserver 10.12.43.11' >> /etc/resolv.conf  "  % password
          a=pool.apply_async(ssh, (ipaddr,conn_port,username, password,cmd, ))
          result[ipaddr]=a
pool.close()
pool.join()

number=0
#print  '##############'
for  k,v in result.items():
 #    print '\033[32m[%s]\033[0m'  %k
     number=number+1
   #  print 'number %s machine output:\n ' %number
     #print  v.get()
     #print k
     for content in  v.get():
         #print k
         print content
