# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 13:10:33 2019

@author: tswayzee
"""

#==========Import Libraries==================

import requests
import json
from datetime import datetime, timedelta
import ftplib
import os

#==========Configio API==================

def get_course_url():
    startdate = datetime.now().strftime("%m/%d/%Y")
    # timedelta() is the amount of days from todays date
    enddate = (datetime.now() + timedelta(days=30)).strftime("%m/%d/%Y")
    return f"https://api.configio.com/api/v1/products?startdate={startdate}&enddate={enddate}"

def get_url_response(url, local_file):
    payload = {}
    headers = {
      'Content-Type': "application/json",
      # Insert Configio API token as a string
      'x-token': '''API TOKEN HERE''',
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    if response.status_code != 200:
        # if failed, create error_log file
        return update_results_file('//we.local/corp/IT/App_Prod/SQL/Python/error_log.php', json.loads(response.text))
    else:
        # if successful, update the configio_api file
        return update_results_file(local_file, json.loads(response.text))

def update_results_file(file_name, results):
    with open(file_name, 'w') as connection_file:
        json.dump(results, connection_file)

    
#==========FTP===========

def connect_to_server():
    server = ftplib.FTP()
    # Get IP, Username, Password from 1password.com
    server.connect(#IP ADDRESS)
    server.login('''USERNAME, PASSWORD''')
    return server

def transfer_local_file_to_ftp(local_file, ftp_path):
    # create local file
    get_url_response(get_course_url(), local_file)
    
    # connect to server
    server = connect_to_server()
    server.cwd(ftp_path)
    
    # transfer the local file to server
    with open(local_file, 'rb') as f:
        server.storbinary(f'STOR {os.path.basename(local_file)}', f, 1024)
        f.close()
    
    # close connection
    server.quit()



transfer_local_file_to_ftp('//we.local/corp/IT/App_Prod/SQL/Python/configio_api.php', 'svy/wp-connection')
    

# to display json to php: https://www.taniarascia.com/how-to-use-json-data-with-php-or-javascript/
