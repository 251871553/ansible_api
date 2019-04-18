#!/bin/env python
from MyAnsible_api import AnsibleApi
from MyMariadb_api import Mariadb_api
import json
import sys
import math

mymariadb=Mariadb_api()



myansible = AnsibleApi('inventory.py')


def run_cmd(host,addition,db_field):
    myansible.runansible(host,'shell',addition)
    result=myansible.get_result()
    result=result['success']
    for k,v in result.items():
        print k,v
        v=v["stdout_lines"]
        stdout_list="$".join(v)
        sql_cmd="update jiqi_all set %s='%s' where ipaddr='%s'" % (db_field,stdout_list,k)
        #print sql_cmd
        mymariadb.update_db(sql_cmd)

addition='cat /etc/crontab | grep -v "#" | grep -v "^$" | grep -v "^SHELL" | grep -v "^PATH"  | grep -v "^MAILTO" | grep -v "^HOME"'
run_cmd('all',addition,'crontab_list')
