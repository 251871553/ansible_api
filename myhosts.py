#!/bin/env python
#coding:utf8
import json
import sys
from MyMariadb_api import Mariadb_api

mymariadb=Mariadb_api()


def group():
    select_sql = "SELECT  DISTINCT group_type  FROM jiqi_all ;"
    groups_list = mymariadb.select_db(select_sql)
    group_data=[]
    for group_name in groups_list:
        group_name=group_name[0].encode('utf-8')
        group_data.append(group_name)
    return group_data

def all():
    all_data={}
    groups_list=group()
    for group_name in groups_list:
        group_name=group_name
        tmp_list=[]
        #select_sql_ip="SELECT  ip   FROM jiqi_all where group_type='%s'  and id >=498 and id <=502;" % group_name
       # select_sql_ip="SELECT  ipaddr   FROM jiqi_all where group_type='%s' and conn_code=0  and id >=1 and id <=100;" % group_name
        select_sql_ip="SELECT  ipaddr   FROM jiqi_all where group_type='%s' and conn_code=0  and id >=100 and id <=200;" % group_name
       # select_sql_ip="SELECT  ip   FROM jiqi_all where group_type='%s';" % group_name
        ip_info = mymariadb.select_db(select_sql_ip)
        for i in ip_info:
            i= i[0].encode('utf-8')
            tmp_list.append(i)
        group_dict={group_name:tmp_list}
        all_data.update(group_dict)
    print(json.dumps(all_data,indent=4))
 
def host(ip):
    select_sql = "SELECT  sshport,sshuser,sshpasswd   FROM jiqi_all where ipaddr = '%s' ;"  % ip
    conn_info= mymariadb.select_db(select_sql)[0]
    info_dict = {
          ip:{
            "ansible_ssh_host":ip,
            "ansible_ssh_port":conn_info[0],
            "ansible_ssh_user":conn_info[1],
            "ansible_ssh_pass":conn_info[2] }
    }
    print(json.dumps(info_dict[ip],indent=4))



if len(sys.argv) == 2 and (sys.argv[1] == '--list'):
    all()
elif len(sys.argv) == 2 and (sys.argv[1] == '--group'):
    for i in group():
      print i
elif len(sys.argv) == 3 and (sys.argv[1] == '--host'):
    host(sys.argv[2])
else:
    print("Usage: %s --list or --host <hostname>" % sys.argv[0])
    sys.exit(1)
