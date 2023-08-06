# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 10:31:10 2022

@author: elog-admin
"""

import elog
import urllib3

urllib3.disable_warnings()


def pass_encrypt(plainPWD):
    return elog.logbook._handle_pswd(plainPWD, True)


def main():
    hostname = "https://10.166.16.24"
    port = 8080
    user = "log-robot"
    password = "IchBinRoboter"
    use_ssl = True
    logbook = "demo"
    elog_instance = elog.open(
        hostname=hostname,
        port=port,
        user=user,
        password=pass_encrypt(password),
        use_ssl=use_ssl,
        logbook=logbook,
        encrypt_pwd=(False)
    )

    attr = {'Operator': user}
    message = 'This is a test'
    elog_instance.post(message, attributes=(attr), encoding='HTML')


if __name__ == '__main__':
    main()
