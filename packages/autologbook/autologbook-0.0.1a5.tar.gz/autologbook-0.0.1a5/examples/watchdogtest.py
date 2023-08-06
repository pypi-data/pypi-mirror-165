# -*- coding: utf-8 -*-
"""
Created on Sun May 15 14:09:47 2022

@author: elog-admin
"""

import logging
import os
import time
from pathlib import Path

import urllib3
import watchdog.events
import watchdog.observers

import autologbook

urllib3.disable_warnings()
loglevel = logging.INFO


if __name__ == "__main__":

    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    folderpath = Path("R:\\A226\\Results\\2022\\12456-RADCAS-Bulgheroni")
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

    autologbookEventHandler = autologbook.QuattroELOGProtocolEventHandler(
        autolog)

    observer = watchdog.observers.Observer()
    observer.schedule(autologbookEventHandler, path=folderpath, recursive=True)
    autologbookEventHandler.processAlreadyExistingItems()
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    autologbook.HTMLObject.resetHTMLContent()
    autolog.generateHTML()
    autolog.postELOGMessage(skipAttachements=False)
