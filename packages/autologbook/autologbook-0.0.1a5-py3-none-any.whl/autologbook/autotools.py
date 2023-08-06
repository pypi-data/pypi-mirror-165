# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 11:06:58 2022

@author: elog-admin
"""

import configparser
import logging
import shutil
from pathlib import Path

import elog
from PyQt5 import QtCore

from autologbook import autoconfig

log = logging.getLogger('__main__')


def init(config):
    """
    Itialize module wide global variables.

    Parameters
    ----------
    config : configparser object or string corresponding to a configuratio file
        The configuration object

    Returns
    -------
    None.

    """
    _config = configparser.ConfigParser()
    if isinstance(config, configparser.ConfigParser):
        _config = config
    elif isinstance(config, str):
        if Path(config).exists() and Path(config).is_file():
            _config.read(config)
        else:
            raise ValueError('Unable to initialize the autowatch-gui module because '
                             + 'the provided configuration file (%s) doesn\'t exist' %
                             (config))
    elif isinstance(config, Path):
        if config.exists() and config.is_file():
            _config.read(str(config))
        else:
            raise ValueError(
                'Unable to initialize the autowatch-gui module because the provided '
                + 'configuration file (%s) doesn\'t exist' % config)
    else:
        raise TypeError(
            'Unable to initialize the autowatch-gui module because of wrong config file')

    # TODO: this code can be refurbished

    autoconfig.ELOG_USER = _config['elog'].get('elog_user',
                                               autoconfig.ELOG_USER)

    autoconfig.ELOG_PASSWORD = _config['elog'].get('elog_password',
                                                   autoconfig.ELOG_PASSWORD)

    autoconfig.ELOG_HOSTNAME = _config['elog'].get('elog_hostname',
                                                   autoconfig.ELOG_HOSTNAME)

    autoconfig.ELOG_PORT = int(_config['elog'].get('elog_port',
                                                   autoconfig.ELOG_PORT))

    autoconfig.USE_SSL = _config.getboolean(
        'elog', 'use_ssl', fallback=autoconfig.USE_SSL)

    autoconfig.MAX_AUTH_ERROR = int(_config['elog'].get(
        'max_auth_error', autoconfig.MAX_AUTH_ERROR))

    autoconfig.NOTEPAD_BEST = Path(_config['external tools'].
                                   get('favourite text editor',
                                       autoconfig.NOTEPAD_BEST))

    autoconfig.ROBOCOPY_EXE = Path(_config['external tools'].
                                   get('robocopy',
                                       autoconfig.ROBOCOPY_EXE))

    autoconfig.MAX_AUTH_ERROR = int(_config['elog'].get(
        'max_auth_error', autoconfig.MAX_AUTH_ERROR))

    autoconfig.AUTOLOGBOOK_WATCHDOG_MAX_ATTEMPTS = int(_config['Autologbook watchdog'].get(
        'max_attempts', autoconfig.AUTOLOGBOOK_WATCHDOG_MAX_ATTEMPTS))

    autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MIN = float(
        _config['Autologbook watchdog'].get('wait_min', autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MIN))

    autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MAX = float(
        _config['Autologbook watchdog'].get('wait_max', autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_MAX))

    autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_INCREMENT = float(_config['Autologbook watchdog'].get(
        'wait_increment', autoconfig.AUTOLOGBOOK_WATCHDOG_WAIT_INCREMENT))

    autoconfig.AUTOLOGBOOK_WATCHDOG_MIN_DELAY = float(_config['Autologbook watchdog'].get(
        'minimum delay between ELOG post', autoconfig.AUTOLOGBOOK_WATCHDOG_MIN_DELAY))

    autoconfig.AUTOLOGBOOK_WATCHDOG_TIMEOUT = _config.getfloat('Autologbook watchdog', 'observer_timeout',
                                                               fallback=autoconfig.AUTOLOGBOOK_WATCHDOG_TIMEOUT)

    autoconfig.AUTOLOGBOOK_MIRRORING_MAX_ATTEMPTS = int(_config['Mirroring watchdog'].get(
        'max_attempts', autoconfig.AUTOLOGBOOK_MIRRORING_MAX_ATTEMPTS))

    autoconfig.AUTOLOGBOOK_MIRRORING_WAIT = float(
        _config['Mirroring watchdog'].get('wait', autoconfig.AUTOLOGBOOK_MIRRORING_WAIT))

    autoconfig.AUTOLOGBOOK_MIRRORING_TIMEOUT = _config.getfloat('Mirroring watchdog', 'observer_timeout',
                                                                fallback=autoconfig.AUTOLOGBOOK_MIRRORING_TIMEOUT)

    autoconfig.IMAGE_SERVER_BASE_PATH = _config['Image_server'].get(
        'base_path', autoconfig.IMAGE_SERVER_BASE_PATH)

    autoconfig.IMAGE_SERVER_ROOT_URL = _config['Image_server'].get(
        'server_root', autoconfig.IMAGE_SERVER_ROOT_URL)

    autoconfig.IMAGE_SAMPLE_THUMB_MAX_WIDTH = int(_config['Image_server'].get(
        'image_thumb_width', autoconfig.IMAGE_SAMPLE_THUMB_MAX_WIDTH))

    autoconfig.CUSTOMID_START = _config.getint(
        'Image_server', 'custom_id_start', fallback=autoconfig.CUSTOMID_START)

    autoconfig.CUSTOMID_TIFFCODE = _config.getint(
        'Image_server', 'tiff_tag_code', fallback=autoconfig.CUSTOMID_TIFFCODE)

    autoconfig.IMAGE_NAVIGATION_MAX_WIDTH = int(_config['Quattro'].get(
        'image_navcam_width', autoconfig.IMAGE_NAVIGATION_MAX_WIDTH))

    autoconfig.QUATTRO_LOGBOOK = _config['Quattro'].get(
        'logbook', autoconfig.QUATTRO_LOGBOOK)

    autoconfig.VERSA_LOGBOOK = _config['Versa'].get(
        'logbook', autoconfig.VERSA_LOGBOOK)


def generate_default_conf():
    """
    Generate a default configuration object.

    Parameters
    ----------
    filename : string or path-like, optional
        The name of the configuration file.
        The default is 'autolog-conf.ini'.

    Returns
    -------
    None.

    """
    config = configparser.ConfigParser(allow_no_value=True)
    config.add_section('elog')
    config['elog'] = {
        'elog_user': 'log-robot',
        'elog_password': encrypt_pass('IchBinRoboter'),
        'elog_hostname': 'https://10.166.16.24',
        'elog_port': '8080',
        'use_ssl': True,
        'use_encrypt_pwd': True,
        'max_auth_error': 5,
        '; To manually insert a (plain text) password, set use_encrypt_pwd to False.': ''
    }
    config['external tools'] = {
        'favourite text editor': 'C:\\Program Files\\Notepad++\\notepad++.exe',
        'robocopy': shutil.which('robocopy.exe')
    }
    config['Quattro'] = {
        'logbook': 'Quattro-Analysis',
        'image_navcam_width': '500'
    }
    config['Versa'] = {
        'logbook': 'Versa-Analysis'
    }
    config['Mirroring engine'] = {
        'engine': 'watchdog'
    }
    config['Autologbook watchdog'] = {
        'max_attempts': '5',
        'wait_min': '1',
        'wait_max': '5',
        'wait_increment': '1',
        'minimum delay between ELOG post': '45',
        'observer_timeout': 0.5
    }
    config['Mirroring watchdog'] = {
        'max_attempts': '2',
        'wait': '0.5',
        'observer_timeout': 0.2
    }
    config['Image_server'] = {
        'base_path': 'R:\\A226\\Results',
        'server_root': 'https://10.166.16.24/micro',
        'image_thumb_width': 400,
        'custom_id_start': 1000,
        'tiff_tag_code': 37510
    }
    return config


def safe_configread(conffile):
    """
    Read the configuration file in a safe manner.

    This function is very useful to read in configuration file checking that
    all the relevant sections and options are there.

    The configuration file is read with the standard configparser.read method
    and a configuration object with all default sections and options is
    generated.

    The two configuration objects are compared and if a section in the read
    file is missing, then it is taken from the default.

    If any addition (section or option) was requested than the integrated
    configuration file is saved to the input file so that the same issue should
    not happen anymore.

    Parameters
    ----------
    conffile : path-like or string
        The filename of the configuration file to be read.

    Returns
    -------
    config : configparser.ConfigParser
        A ConfigParser object containing all sections and options required.

    """
    config = configparser.ConfigParser()
    config.read(conffile)

    # check if it is an old configuration file with plain text password
    if not config.has_option('elog', 'use_encrypt_pwd'):
        config['elog']['elog_password'] = encrypt_pass(
            config['elog']['elog_password'])

    # now we must check that we have everything
    conffile_needs_updates = False
    default_config = generate_default_conf()
    for section in default_config.sections():
        if not config.has_section(section):
            config.add_section(section)
            conffile_needs_updates = True
            log.info('Section %s is missing from configuration file %s. The default values will be used and the file updated' %
                     (section, conffile))
        for option in default_config.options(section):
            if not config.has_option(section, option):
                config.set(section, option, default_config[section][option])
                conffile_needs_updates = True
                log.info('Option %s from section %s is missing. The default value will be used and the file update' %
                         (option, section))

    if not config.getboolean('elog', 'use_encrypt_pwd'):
        # it looks like the user changed manually the configuration file introducing a
        # plain text password.
        # we need to hash the password and update the configuration file
        config['elog']['use_encrypt_pwd'] = "True"
        config['elog']['elog_password'] = encrypt_pass(
            config['elog']['elog_password'])
        conffile_needs_updates = True

    if conffile_needs_updates:
        with open(conffile, 'w') as f:
            config.write(f)

    return config


def write_default_conffile(filename='autolog-conf.ini'):
    """
    Write the default configuration object to a file.

    Parameters
    ----------
    filename : path-like object, optional
        The filename for the configuration file.
        The default is 'autolog-conf.ini'.

    Returns
    -------
    None.

    """
    config = generate_default_conf()
    with open(filename, 'w') as configfile:
        config.write(configfile)


def parents_list(actual_path, base_path):
    """
    Generate the parents list of a given image.

    This tool is used to generate of a list of parents pairs.
    Let's assume you are adding a new image with the following path:
        actual_path = R:/A226/Results/2022/123 - proj - resp/SampleA/SubSampleB/SubSampleC/image.tiff
    and that the protocol folder is located at:
        base_path = R:/A226/Results/2022/123 - proj - resp/

    This function is returning the following list:
        [ (SampleA, None),
          (SubSampleB, SampleA),
          (SubSampleC, SubSampleB)
         ]

    It is to say a list of pairs in which the first element is the sample and the second element
    is its parent. In the case of a top level sample, is parent is set to None.

    Parameters
    ----------
    actual_path : string or Path
        The full path (including the filename) of the pictures being considered.
    base_path : string or Path
        The path of the protocol.

    Returns
    -------
    parents_list : List of pairs
        A list of parent pairs. See the function description for more details.

    """
    if not isinstance(actual_path, Path):
        actual_path = Path(actual_path)

    if not isinstance(base_path, Path):
        base_path = Path(base_path)

    subtree = actual_path.relative_to(base_path)
    log.debug('The subtree for %s is %s' % (actual_path, subtree))

    parents_list = []
    for i in range(len(subtree.parents[0].parts)):
        if i == 0:
            parents_list.append((subtree.parents[0].parts[i], None))
        else:
            parents_list.append((subtree.parents[0].parts[i],
                                 subtree.parents[0].parts[i - 1]))

    return parents_list


def decodeCommandOutput(text):
    """
    Decode the output of a command started with Popen.

    Parameters
    ----------
    text : STRING
        The text produced by Popen and to be decoded.

    Returns
    -------
    STRING
        The decoded text.

    """
    return '\n'.join(text.decode('utf-8').splitlines())


def ctname():
    """
    Return the current QThread name.

    Returns
    -------
    STRING
        The name of the current QThread.

    """
    return QtCore.QThread.currentThread().objectName()


class literal_str(str):
    """Type definition for the YAML representer."""

    pass


def change_style(style, representer):
    """
    Change the YAML dumper style.

    Parameters
    ----------
    style : String
        A string to define new style.
    representer : SafeRepresenter
        The yaml representer of which the style should be changed

    Returns
    -------
    Callable
        The new representer with the changed style.

    """

    def new_representer(dumper, data):
        """
        Return the new representer.

        Parameters
        ----------
        dumper : TYPE
            DESCRIPTION.
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        scalar : TYPE
            DESCRIPTION.

        """
        scalar = representer(dumper, data)
        scalar.style = style
        return scalar
    return new_representer


def my_excepthook(excType, excValue, traceback, logger=log):
    """Define a customized exception hook.

    Instead of printing the output of an uncaught exception to the stderr,
    it is redirected to the logger. It is very practical because it will
    appear on the GUI

    Parameters
    ----------
    excType : TYPE
        The exception type.
    excValue : TYPE
        The exception value.
    traceback : TYPE
        The whole traceback.
    logger : TYPE, optional
        The logger instance where the exception should be sent.
        The default is log.

    Returns
    -------
    None.

    """
    logger.error("Logging an uncaught exception",
                 exc_info=(excType, excValue, traceback))


def encrypt_pass(plainTextPWD):
    """
    Encrypt a plain text password.

    In order to avoid exposure of plain text password in the code, this
    helper function can be used to store hashed password directly usable for
    the elog connection.

    Parameters
    ----------
    plainTextPWD : string
        The plain text password as introduced by the user to be encrypted.

    Returns
    -------
    string
        The hashed password to be used directly in the elog connect method.

    """
    return elog.logbook._handle_pswd(plainTextPWD, True)
