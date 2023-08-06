# -*- coding: utf-8 -*-
"""
Created on Mon May 23 09:30:59 2022

@author: elog-admin
"""

import logging
import time
from pathlib import Path

import watchdog.events
import watchdog.observers

import autologbook

if __name__ == '__main__':

    log = logging.getLogger(__name__)
    logging.basicConfig(format="%(levelname)s: %(message)s", level=10)

    src = Path('C:/Users/elog-admin/Documents/src/12456-RADCAS-Bulgheroni')
    dest = Path('R:/A226/Results/2022/12456-RADCAS-Bulgheroni')

    mirroringHandler = autologbook.MirroringHandler(src, dest)

    observer = watchdog.observers.Observer()
    observer.schedule(mirroringHandler, path=str(src), recursive=True)
    mirroringHandler.process_all_existing()
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
