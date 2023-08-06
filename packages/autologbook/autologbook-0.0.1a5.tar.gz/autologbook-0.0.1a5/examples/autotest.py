
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 14:58:17 2022

@author: elog-admin
"""

import glob
import logging
import os
from datetime import datetime

import elog
import urllib3

import autologbook

urllib3.disable_warnings()
loglevel = logging.INFO


def main():

    # logging
    # logger = logging.getLogger(__name__)
    # logger.setLevel(loglevel)

    # # create console handler
    # ch = logging.StreamHandler()
    # ch.setLevel(loglevel)

    # # formatter
    # formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

    # # add formatter to console handler
    # ch.setFormatter(formatter)

    # # add console handler to the logger
    # logger.addHandler(ch)
    # logger.debug('messaggio')

    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    folderpath = os.path.join(
        "R:\\A226\\Results\\2022\\12456-RADCAS-Bulgheroni")
    elog_hostname = 'https://10.166.16.24/'
    elog_port = 8080
    elog_use_ssl = True
    elog_user = 'log-robot'
    elog_password = 'IchBinRoboter'
    elog_encoding = 'HTML'

    autolog = autologbook.QuattroELOGProtocol(
        path=folderpath,
        elog_hostname=elog_hostname,
        elog_port=elog_port,
        elog_user=elog_user,
        elog_password=elog_password)
    autologbook.HTMLObject.resetHTMLContent()

    for item in glob.glob(os.path.join(folderpath, '*Nav?am*')):
        autolog.addNavCam(item)

    for item in glob.glob(os.path.join(folderpath, '*')):
        if os.path.isdir(item):
            sample = autologbook.Sample(name=os.path.split(item)[-1])
            for tiffimage in glob.glob(os.path.join(item, '*tif*')):
                sample.addMicroscopePicture(
                    autologbook.QuattroFEIPicture(tiffimage))
            autolog.addSample(sample)

    logging.info('The protocol contains {} samples'.format(
        len(autolog.samples)))

    autolog.generateHTML()
    autolog.saveHTML2File('myfile.html')
    # print(autolog.printHTML(True))
    autolog.postELOGMessage()


if __name__ == '__main__':
    main()
