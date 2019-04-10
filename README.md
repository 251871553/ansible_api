# ansible_api
collection information of machine  to the mariadb by ansible_api 
table structure
MariaDB [ansible_inv]> desc  jiqi_all;
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | int(11)      | NO   | PRI | NULL    | auto_increment |
| ipaddr     | varchar(255) | YES  |     | NULL    |                |
| sshport    | varchar(255) | YES  |     | NULL    |                |
| sshuser    | varchar(255) | YES  |     | NULL    |                |
| sshpasswd  | varchar(255) | YES  |     | NULL    |                |
| conn_code  | varchar(255) | YES  |     | NULL    |                |
| group_type | varchar(255) | YES  |     | NULL    |                |
| hostname   | varchar(255) | YES  |     | NULL    |                |
| os_type    | varchar(255) | YES  |     | NULL    |                |
| os_distrib | varchar(255) | YES  |     | NULL    |                |
| os_version | varchar(255) | YES  |     | NULL    |                |
| os_kernel  | varchar(255) | YES  |     | NULL    |                |
| cpu_count  | int(255)     | YES  |     | NULL    |                |
| mem_total  | int(255)     | YES  |     | NULL    |                |
| disk_total | int(255)     | YES  |     | NULL    |                |
| dns_list   | varchar(255) | YES  |     | NULL    |                |
| ip_v4_list | varchar(255) | YES  |     | NULL    |                |
+------------+--------------+------+-----+---------+----------------+
17 rows in set (0.00 sec)
