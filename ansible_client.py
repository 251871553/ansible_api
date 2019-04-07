from MyAnsible_api import AnsibleApi
from MyMariadb_api import Mariadb_api
import json

mymariadb=Mariadb_api()
myansible = AnsibleApi('/data/hosts')
#myansible.runansible('192.168.3.130','setup','filter=ansible_facts')
myansible.runansible('all','setup','')
result=myansible.get_result()
#result=result['success']['192.168.3.130']["ansible_facts"]
result=result['success']
for k,v in result.items():
    v=v["ansible_facts"]
    dns_list=v['ansible_dns']['nameservers']
    dns_list=",".join(dns_list)
    ipv4_list=v['ansible_all_ipv4_addresses']
    ipv4_list=",".join(ipv4_list)
    sql_cmd="update cmdb set hostname='%s',os_type='%s',os_distrib='%s',os_version='%s',os_kernel='%s',cpu_count='%d',mem_all='%d',dns_all='%s',ip_v4_all='%s' where ipaddr='%s'" % (v['ansible_hostname'],v['ansible_system'],v['ansible_distribution'],v['ansible_distribution_version'],v['ansible_kernel'],v['ansible_processor_count'],v['ansible_memtotal_mb'],dns_list,ipv4_list,k)
    #print sql_cmd
    mymariadb.update_db(sql_cmd)
#result=result['success'].keys()
#print type(result)
#print result
#print json.dumps(result,indent=4)
#print json.dumps(result,indent=4)
#myansible.playbookrun(playbook_path=['/data/test.yml'])
