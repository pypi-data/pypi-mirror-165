# -*- coding: utf-8 -*-
"""
Created on Fri May 27 11:04:20 2022

@author: elog-admin
"""

import configparser

config = configparser.ConfigParser()
config['elog'] = {
    'elog_user': 'log-robot',
    'elog_password': 'IchBinRoboter',
    'elog_hostname': 'https://10.166.16.24',
    'elog_port': 8080,
    'elog_use_ssl': True
}

config['quattro'] = {
    'logbook': 'Quattro-Analysis'
}

config['yaml-editor'] = {
    'fav_editor_path': 'C:\\Program Files\\Notepad++\\notepad++.exe'
}

config['watchdog'] = {
    'mirroring_engine': 'robocopy',
    'shared_base_path': 'R:\\A226\\Results'


}
