# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 12:48:58 2022

@author: elog-admin
"""

import elog
import urllib3

urllib3.disable_warnings()

def main():
    hostname = "https://10.166.16.24"
    port = 8080
    user = "bulghao"
    password = "PorcaVacca"
    use_ssl = True
    logbook = "demo"
    elog_instance = elog.open(
        hostname = hostname,
        port = port,
        user = user,
        password = password,
        use_ssl = use_ssl,
        logbook = logbook
        )
    
    
    attributes = { 'Mass' : 1, 'Sample material' : 'Però'}
    
    message = ''
    with open('test_accents.txt', 'rt', encoding='utf-8') as file:
        message = file.read()
    
    attach = ['test_accents.txt']
    attributes = {k: str(v).encode('utf-8') for k,v in attributes.items()}
    
    elog_instance.post(message,  reply=False, attributes=attributes,encoding='HTML')
    
if __name__ == '__main__':
    main()