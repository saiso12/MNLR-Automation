
import ast
import paramiko
import sys
import os
import re
import time
import subprocess



def collect_info(info_file, user, code_dir):
    '''
    Read the dev info from the file and form a dictionary
    :return:
    '''
    my_dict = eval(open(info_file).read())

    ssh = []
    for i in range(0, len(my_dict)):
        ssh.append(paramiko.SSHClient())

    print ssh
    print "Number of Nodes: {0}".format(len(my_dict))
    print "RIT username : {0}".format(user)

    #try to copy the latest MNLR code from the execution server to each of the
    #nodes in the GENI
    for node in range(0, len(my_dict)):
        dic_val = "node-" + str(node)
        conn_info = my_dict[dic_val]
        scp_cmd = "scp -i ~/.ssh/id_geni_ssh_rsa -P {0} -r {1} {2}@{3}:/users/{4}".format(conn_info[1], code_dir, user, conn_info[0], user)
        proc = subprocess.Popen(scp_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        op, err = proc.communicate()
        print op, err
        time.sleep(3)
        match = re.search("(yes/no)", op)
        if match:
            print match.group()
            os.system("yes")
            time.sleep(10)
        print "Copied to {0}".format(dic_val)

