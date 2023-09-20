#######################################################################
# Copyright (c) 2022 cisco Systems, Inc. - All Rights Reserved
# Unauthorized copying of this file,
# via any medium is strictly prohibited
# Proprietary and confidential
#######################################################################
__author__ = " Vishwajeeth Mandalika, Keyshawn Taylor"
__copyright__ = "Copyright 2022, cisco Systems, Inc"
__credits__ = ["Vishwajeeth Mandalika"]
__version__ = "1.0.0"
__maintainer__ = " Vishwajeeth Mandalika"
__email__ = " vmadalik@cisco.com"
__status__ = "Development"

try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain

# from asyncio.windows_events import NULL
# from pickle import NONE
# from queue import Empty

import requests
import json
import urllib3
import os
import csv
import getpass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
while True:
    filenamecsv = input(
        "Enter the path of the CSV files with APIC IPs, Usernames and Password:"
    )
    if os.access(filenamecsv, os.W_OK):
        break
    print(filenamecsv, "is not a valid path")
print(filenamecsv, "is a valid path")


def apic_login(apic: str, username: str, password: str) -> dict:
    credentials = {"aaaUser": {"attributes": {"name": username, "pwd": password}}}
    json_credentials = json.dumps(credentials)
    base_url = "https://" + apic_url + "/api/aaaLogin.json"
    login_response = requests.post(base_url, data=json_credentials, verify=False)
    login_response_json = json.loads(login_response.text)
    token = login_response_json["imdata"][0]["aaaLogin"]["attributes"]["token"]
    apic_cookie["APIC-Cookie"] = token
    print("\nLogging into APIC " + row[0])
    return apic_cookie


def apic_query(apic: str, path: str, cookie: dict):
    print("Querying...")
    base_url = "https://" + apic_url + path
    # print(base_url)
    get_response = requests.get(base_url, cookies=cookie, verify=False)
    # print(get_response.text)
    faultcheck = get_response.text
    # print(faultcheck)
    with open(apic_url + "_" + row[2] + ".xml", "w") as foutput:
        foutput.write(faultcheck)


def apic_logout(apic: str, cookie: dict):
    base_url = "https://" + apic_url + "/api/aaaLogout.json"
    post_response = requests.post(base_url, cookies=cookie, verify=False)
    print("Logging out of APIC " + row[0])


with open(filenamecsv, newline="") as csvfile:
    csvreader = csv.reader(csvfile)
    # print(type(csvreader))
    for row in csvreader:
        apic_url = row[0]
        username = row[1]
        if not row[3]:
            print("The password cell in the CSV file is empty for the APIC" + apic_url)
            print("********Typed Password will not show for security*******")
            password = getpass.getpass("Enter password for the APIC " + apic_url + ":")
        else:
            password = row[3]
        path = "/api/class/faultInfo.xml"
        path2 = "/api/class/topSystem.json"
        apic_cookie = {}
        faultcheck = str()

        try:
            apic_login(apic_url, username, password)
            apic_query(apic_url, path, apic_cookie)
            apic_logout(apic_url, apic_cookie)
        except Exception as e:
            print(e)


print(
    "\n*******************************************************************************"
)
print(
    "The files are stored in the same directory from where you are RUNNING this script "
    + os.getcwd()
)


################################################################
# The following code can help perform the same task as
# above but with input being a XLS file (version 97 to 2003)
################################################################

"""
import xlrd
filename= "C:/Users/vmadalik/Downloads/PowerShellPython/ACI fault Report/ACIFaultCollection/APICIPs.xls"
wb = xlrd.open_workbook(filename,ragged_rows=True)
sh = wb.sheet_by_index(0)
x=[]
for rownum in range(sh.nrows):
    if((sh.row_values(rownum))) != []:
       x.append((sh.row_values(rownum)))

for i in range(1, sh.nrows):
    apic_url = x[i][0]
    username = x[i][1]
    if not row[3]:
            print("The password cell in the CSV file is empty for the APIC"+ apic_url)
            print("********Typed Password will not show for security*******")
            password = getpass.getpass("Enter password for the APIC "+ apic_url + ":")
    else:
            password = row[3]
    path = "/api/class/faultInfo.xml"
    apic_cookie = {}
    faultcheck = str()

    def apic_login(apic:str, username:str, password:str) -> dict:
        credentials = {'aaaUser': {'attributes': {'name': username, 'pwd': password }}}
        json_credentials = json.dumps(credentials)
        base_url = 'https://' + apic_url + '/api/aaaLogin.json'
        login_response = requests.post(base_url, data=json_credentials, verify=False)
        login_response_json = json.loads(login_response.text)
        token = login_response_json['imdata'][0]['aaaLogin']['attributes']['token']
        apic_cookie['APIC-Cookie'] = token
        return apic_cookie

    def apic_query(apic:str, path:str, cookie:dict):
        print("\nquerying")
        base_url = 'https://' + apic_url + path
        print(base_url)
        get_response = requests.get(base_url, cookies=cookie, verify=False)
        faultcheck= (get_response.text)
        #print(faultcheck)
        with open(apic_url+"_"+x[i][2] +'.xml', 'w') as foutput:
            foutput.write(faultcheck)
        
    def apic_logout(apic: str, cookie:dict):
        base_url = 'https://' + apic_url + '/api/aaaLogout.json'
        post_response = requests.post(base_url, cookies=cookie, verify=False)
        print("Logging out of APIC "+ x[i][0] )
        
    def main():    
        
        apic_login (apic_url, username,password)
        apic_query(apic_url, path, apic_cookie)
        apic_logout(apic_url, apic_cookie)
        print("*******************************************************************************")
        print("The files are stored in the same directory from where you are RUNNING this script " +os.getcwd())

    if __name__ == '__main__':
        main()"""
