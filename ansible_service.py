#!/bin/env python
from MyAnsible_api import AnsibleApi
from MyMariadb_api import Mariadb_api
import json
import sys
import math

mymariadb=Mariadb_api()



#myansible = AnsibleApi('hosts')
myansible = AnsibleApi('inventory.py')


def run_cmd(host,db_field,addition):
    myansible.runansible(host,'shell',addition  )
    result=myansible.get_result()
    succ=result["success"]
    fail=result["failed"]
    unreach=result["unreachable"]
    if succ:
       succ_status=0
       for succ_ip in succ.keys():
          sql_cmd="update jiqi_service set %s='%s' where id=(SELECT id FROM jiqi_all WHERE ipaddr='%s')" % (db_field,succ_status,succ_ip)
          print sql_cmd
          mymariadb.update_db(sql_cmd)
    if fail:
       for k,v in fail.items():
           if v=='non-zero return code':
              service_status=1
              #print k,service_status
              sql_cmd="update jiqi_service set %s='%s' where id=(SELECT id FROM jiqi_all WHERE ipaddr='%s')" % (db_field,service_status,k)
     #         print sql_cmd
              mymariadb.update_db(sql_cmd)
           else:
              service_status=2
              sql_cmd="update jiqi_service set %s='%s' where id=(SELECT id FROM jiqi_all WHERE ipaddr='%s')" % (db_field,service_status,k)
             # print sql_cmd
              mymariadb.update_db(sql_cmd)
              #print k,service_status
    if unreach:
       service_status=3
       for unreach_ip in unreach.keys():
        sql_cmd="update jiqi_all set %s='%s' where ipaddr='%s'" % (db_field,stdout_list,unreach_ip)
        #print sql_cmd
        mymariadb.update_db(sql_cmd)

nginx='ps aux | grep nginx | grep -v grep '
postgre='ps aux | grep postgre | grep -v grep '
redis_server='ps aux | grep redis-server | grep -v grep '
redis_sentinel='ps aux | grep redis-sentinel | grep -v grep '
memcached='ps aux | grep memcached | grep -v grep '
keepalived='ps aux | grep keepalived | grep -v grep '
haproxy='ps aux | grep haproxy | grep -v grep '
zookeeper='ps  aux  | grep   java | grep  zookeeper | grep -v grep'
tomcat='ps -aux |grep java | grep tomcat | grep -v zookeeper   | grep -v grep'
service_dict={'nginx':nginx,'postgre':postgre,'redis_server':redis_server,'redis_sentinel':redis_sentinel,'memcached':memcached,'keepalived':keepalived,'haproxy':haproxy,'zookeeper':zookeeper,'tomcat':tomcat}
#service_dict={'nginx':nginx}
print service_dict
for k,v in service_dict.items():
    run_cmd('all',k,v)
