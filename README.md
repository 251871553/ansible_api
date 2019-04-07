# ansible_api
collection information of machine  to the mariadb by ansible_api 
table structure
MariaDB [cmdb]> desc cmdb;
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | int(11)      | NO   | PRI | NULL    | auto_increment |
| ipaddr     | varchar(255) | NO   |     | NULL    |                |
| hostname   | varchar(255) | YES  |     | NULL    |                |
| os_type    | varchar(255) | YES  |     | NULL    |                |
| os_distrib | varchar(255) | YES  |     | NULL    |                |
| os_version | varchar(255) | YES  |     | NULL    |                |
| os_kernel  | varchar(255) | YES  |     | NULL    |                |
| cpu_count  | int(255)     | YES  |     | NULL    |                |
| mem_all    | int(255)     | YES  |     | NULL    |                |
| dns_all    | varchar(255) | YES  |     | NULL    |                |
| ip_v4_all  | varchar(255) | YES  |     | NULL    |                |
+------------+--------------+------+-----+---------+----------------+

