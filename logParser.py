import re
from pandas import *
import numpy

'''
Output in files :
Webaccess LOG1 -  stores logs which do not have access to .jpg,.gif and .css
Webaccess LOG2 - stores logs which have status codes in range [200,299]
Unique Users - stores list of unique users
Histogram is displayed in a separate GUI window
'''

#reading from log file
log_file = open("Webaccess LOG.txt","r")
logs = log_file.read()
log_records = logs.split("\n")

#initializing lists to store individual parts of log file
ip_value_list=[]
time_stamp_list=[]
request_method_list=[]
resource_requested_list = []
status_code_list=[]
bytes_sent_list=[]
address_list=[]
browser_list=[]

# this file stores logs which do not have access to .jpg,.gif and .css
output_log1 = open("Webaccess LOG1.txt","w")

#this file stores logs which have status codes in range [200,299]
output_log2 = open("Webaccess LOG2.txt","w")

for log_record in log_records:
    # matching a log record with regular expression
    pattern = "([0-9\.]*)[ \t]*[0-9]*[ \t]*\-[ \t]*\-[ \t]*\[(.*)\][ \t]*[\"]+([^\"]*)\"[ \t]+\"([^\"]*)\"\"[ \t]+([0-9]+|\-)[ \t]+([0-9]+|\-)[ \t]+\"\"([^\"]*)\"\"[ \t]+\"\"([^\"]*)\"\"\""    
    reg_match = re.match(pattern,log_record,re.DOTALL)
    
    if(not reg_match): # if regular expression does not match with log record i.e. the log record is incomplete(missing data)
        continue
    
    rg = reg_match.group

    # fetch individual values
    ip_value = rg(1)
    time_stamp = rg(2)
    request_method = rg(3)
    resource_requested = rg(4)
    status_code = rg(5)
    bytes_sent = rg(6)
    address = rg(7)
    browser = rg(8)
    
    if bytes_sent.isdigit() : # fetching bytes sent
        bytes_sent = int(bytes_sent)
    else: # if bytes sent has a '-'
        bytes_sent = 0


    # check if resource requested has .jpg .gif .css 
    if(".jpg" in resource_requested or ".JPG" in resource_requested or ".gif" in resource_requested or ".GIF" in resource_requested or ".css" in resource_requested or ".CSS" in resource_requested):
        [] # do nothing
    else:
        output_log1.write(log_record+"\n")

    # check for range of status code
    code = int(status_code)
    if((code>=200 and code <=299)):
        output_log2.write(log_record+"\n")

    # updating lists
    ip_value_list.append(rg(1))
    time_stamp_list.append(rg(2))
    request_method_list.append(rg(3))
    resource_requested_list.append(rg(4))
    status_code_list.append(rg(5))
    bytes_sent_list.append(bytes_sent)
    address_list.append(rg(7))
    browser_list.append(rg(8))

output_log1.close()    
output_log2.close()

# using pandas DataFrame to store mapping between ip address and browser list for effective removal of duplicates
ip_brower_logs = pandas.DataFrame({'1:ip':ip_value_list,'2:browser':browser_list})

unique_users = ip_brower_logs.drop_duplicates()

# finding duplicate users
users = unique_users.get_values()
with open("Unique Users.txt","w") as user_file: # this file stores list of unique users
    for user in users:
        user_file.write(user[0]+"\t"+user[1]+"\n")

#Plotting histogram using DataFrame of bytes sent with indexing of ip address
import matplotlib.pyplot as plt
ip_bytes_logs = pandas.DataFrame({'bytes':bytes_sent_list},index =ip_value_list)
ip_bytes_total=ip_bytes_logs.groupby(ip_bytes_logs.index).sum()
ip_bytes_total.plot(kind='bar')
plt.show()

