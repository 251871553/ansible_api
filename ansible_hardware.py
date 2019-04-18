#!/bin/env python
from MyAnsible_api import AnsibleApi
from MyMariadb_api import Mariadb_api
import json
import sys
import math

mymariadb=Mariadb_api()



#myansible = AnsibleApi('hosts')
myansible = AnsibleApi('inventory.py')
#myansible.runansible('192.168.3.130','setup','filter=ansible_facts')
#myansible.runansible('10.11.38.20','setup','')
#myansible.runansible('10.11.93.220','setup','')
myansible.runansible('all','setup','')
result=myansible.get_result()
#print result
result=result['success']
#sys.exit()
for k,v in result.items():
    print k
    v=v["ansible_facts"]
    try:
       dns_list=v['ansible_dns']['nameservers']
       dns_list=",".join(dns_list)
    except KeyError :
       dns_list=""
    ipv4_list=v['ansible_all_ipv4_addresses']
    ipv4_list=",".join(ipv4_list)
    mem_total=float(v['ansible_memtotal_mb']) / 1024
    mem_total= int(round(mem_total))
    #disk_list=v['ansible_devices']
    disk_total = sum([int(v["ansible_devices"][i]["sectors"]) * \
    int(v["ansible_devices"][i]["sectorsize"]) / 1024 / 1024 / 1024 \
    for i in v["ansible_devices"] if i[0:2] in ("sd", "ss")])
    sql_cmd="update jiqi_all set hostname='%s',os_type='%s',os_distrib='%s',os_version='%s',os_kernel='%s',cpu_count='%d',mem_total='%d',disk_total='%d',dns_list='%s',ip_v4_list='%s' where ipaddr='%s'" % (v['ansible_hostname'],v['ansible_system'],v['ansible_distribution'],v['ansible_distribution_version'],v['ansible_kernel'],v['ansible_processor_vcpus'],mem_total,disk_total,dns_list,ipv4_list,k)
    mymariadb.update_db(sql_cmd)
#result=result['success'].keys()
#print type(result)
#print result
#print json.dumps(result,indent=4)
#myansible.playbookrun(playbook_path=['/data/test.yml'])
