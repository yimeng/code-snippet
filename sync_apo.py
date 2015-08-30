#!./python
from fileinput import filename

__author__ = 'yimeng'
import MySQLdb


class Database:

    db_address = "ipaddress"
    db_user = "user"
    db_password= "password"
    db_database= "db"
    db_port = 3306

    def exec_query(self,sql):
        conn = MySQLdb.connect(host=self.db_address,user=self.db_user,passwd=self.db_password,db=self.db_database)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        return result


class Util:

    @staticmethod
    def result_to_kv(db_result):
        kv_result={}

        for line in db_result:
            kv_result.setdefault(line[1],[]).append(line[0])

        return kv_result


class AnsibleHosts:


    @staticmethod
    def to_file(kv_result):
        file_name = "/usr/home/yimeng3/ansible/hosts"

        file = open(file_name,"w")

        for key in kv_result.keys():
            file.writelines('['+key+']'+'\n')
            for value in kv_result[key]:
                file.writelines(value+'\n')

        file.close()

            # file.writelines(line[0]+'\t'+line[1]+'\n')
class RundeskHost:
    @staticmethod

    def to_file(kv_result):

        file_name = "/tmp/host.txt"
        file = open(file_name,"w")
        file.writelines('<?xml version="1.0" encoding="UTF-8"?>'+"\n") 
        file.writelines('<project>'+"\n")

        for key in kv_result.keys():
            for value in kv_result[key]:
                file.writelines('<node name="'+value+'" description="Rundecknode" tags="'+key+'" hostname="'+value+'" osArch="amd64" osFamily="unix" osName="Linux" osVersion="2.6.32-431.11.2.el6.toa.2.x86_64" username="yimeng3"/>'+"\n") 

        file.writelines('</project>')
        file.close()

class PdshHosts:
    @staticmethod
    def to_file(kv_result):
        for key in kv_result.keys():
            file = open("/data1/users/yimeng3/.dsh/group"+key,"w")

            for value in kv_result[key]:
                file.writelines(value+'\n')

            file.close()

if __name__ == '__main__':

    db = Database()

    result = db.exec_query("SELECT ip,app_pool FROM  app_pool_node")

    kv_result = Util.result_to_kv(result)

    AnsibleHosts.to_file(kv_result)
    PdshHosts.to_file(kv_result)
    RundeskHost.to_file(kv_result)







