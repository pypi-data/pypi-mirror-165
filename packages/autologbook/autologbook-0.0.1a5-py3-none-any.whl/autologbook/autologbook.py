# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 11:01:34 2022

@author: elog-admin
"""

import argparse
import ctypes
import logging
import sys
from pathlib import Path

from autologbook import autocli, autogui, autotools

log = logging.getLogger()
LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warn': logging.WARNING,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}

# use this to catch all exceptions in the GUI
sys.excepthook = autotools.my_excepthook


def main_parser():
    """
    Define the main argument parser.

    Returns
    -------
    parser : ArgumentParser
        The main parser.

    """
    parser = argparse.ArgumentParser(description='''
                                     GUI of the automatic
                                     logbook generation tool for microscopy
                                     ''')
    # Define here all configuration related arguments
    # configuration file, experiment file, mirroring
    confgroup = parser.add_argument_group('Configuration',
                                          '''
                                          The following options allow the user to specify
                                          a configuration file different from the default one
                                          or an experiment file to be loaded.
                                          ''')
    confgroup.add_argument('-c', '--conf-file', type=Path, dest='conffile',
                           default=(Path.cwd() / Path('autolog-conf.ini')),
                           help='Specify a configuration file to be loaded.')
    confgroup.add_argument('-e', '--exp-file', type=Path, dest='expfile',
                           help='Specify an experiment file to be loaded')
    confgroup.add_argument('-x', '--auto-exec', dest='autoexec', action='store_true',
                           help='When used in conjunction with -e, if the start watchdog is '
                           'enabled, the wathdog will be started right away')
    confgroup.add_argument('-m', '--mirroring-engine', type=str, dest='engine',
                           choices=('watchdog', 'robocopy'), default='watchdog',
                           help='''
                        Override the mirroring engine defined in the configuration file
                        either to watchdog
                        (faster and rather stable) or robocopy
                        (slower and very stable)
                        ''')

    # Define here all user interface options
    uigroup = parser.add_argument_group('User interface', '''
                                        Instead of executing the full graphical user interface,
                                        the user may opt for a simplify command line interface
                                        using the options below.\n\n
                                        ** NOTE ** The CLI is still very experimental.
                                        ''')
    uigroup.add_argument('-t', '--cli', dest='cli', action='store_true',
                         help='When set, a simplified command line interface will '
                         'be started. It implies the -x option and it requires '
                         'an experiment file to be specified with -e.\n'
                         'A valid combination is -txe <experiment_file>')
    uigroup.add_argument('-l', '--log', dest='loglevel',
                         choices=('debug', 'info', 'warning',
                                  'error', 'critical'),
                         default='info',
                         help='''
                        The verbosity of the logging messages.
                        ''')

    # Define here all authentication options
    authgroup = parser.add_argument_group('Authentication', '''
                                          Override the username and password settings in the
                                          configuration file. If the user provides only a username
                                          the password in the configuration will not be used.
                                          If no password is given with option -p, a dialog window
                                          will ask for the user credentials when need it.
                                          The user must enter his/her password as plain text from
                                          the command line.\n
                                          '''
                                          '''
                                          **NOTE**
                                          Credentials stored in experiment files are not overriden!
                                          ''')
    authgroup.add_argument('-u', '--user', type=str, dest='username',
                           help='Specify the username to be used for the connection to the ELOG. '
                           + 'When this flag is used, the user must provide a password either via '
                           + 'the -p flag or via the GUI when prompted.')
    authgroup.add_argument('-p', '--password', type=str, dest='password',
                           help='Specify the password to be used for the connection to the ELOG. '
                           + 'If a username is not provided via the -u flag, the username in the '
                           + 'configuration file will be used.')

    return parser


def main(cli_args, prog):
    """
    Define main function to start the event loop.

    Returns
    -------
    None.

    """
    # get the cli args from the parser
    parser = main_parser()
    if prog:
        parser.prog = prog

    args = parser.parse_args(cli_args)

    # to set the icon on the window task bar
    myappid = u'ecjrc.autologook.gui.v1.0.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    if args.cli:
        autocli.main_cli(args)
    else:
        autogui.main_gui(args)
