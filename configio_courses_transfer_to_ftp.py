# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 13:10:33 2019

@author: tswayzee
"""

#==========Import Libraries==================

import requests
import json
from datetime import datetime, timedelta
import pysftp

#==========Configio API==================

def get_course_url():
    startdate = datetime.now().strftime("%m/%d/%Y")
    # timedelta() is the amount of days from todays date
    enddate = (datetime.now() + timedelta(days=180)).strftime("%m/%d/%Y")
    return f"https://api.configio.com/api/v1/products?startdate={startdate}&enddate={enddate}"

def get_url_response(url, local_file):
    payload = {}
    headers = {
      'Content-Type': "application/json",
      'x-token': API_TOKEN,
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

    
#============SFTP==============

def transfer_local_file_to_ftp(local_file, ftp_path):
    # create local file
    get_url_response(get_course_url(), local_file)
    
    # connect to server
    cnopts = pysftp.CnOpts(knownhosts='~/.ssh/authorized_keys')
    cnopts.hostkeys = None
    
    with pysftp.Connection(IP_ADDRESS, username=USERNAME, private_key=KEY_PATH_TO_KEY, private_key_pass=PASSWORD, cnopts=cnopts) as server:
        server.chdir(ftp_path)
        server.put(local_file)
    
        # close connection
        server.close()


# RUN!
transfer_local_file_to_ftp('//we.local/corp/IT/App_Prod/SQL/Python/configio_api.php', 'public_html/svy/wp-connection')


# to display json to php: https://www.taniarascia.com/how-to-use-json-data-with-php-or-javascript/