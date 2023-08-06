# -*- coding: utf-8 -*-

"""
Created on Sat May 21 12:10:26 2022

@author: elog-admin
"""

import configparser
import logging
import os
import re
import shutil
import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path

import elog
import urllib3
import watchdog.events
import watchdog.observers
import yaml
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import QItemSelection, QModelIndex, QStandardItem, QStandardItemModel
from PyQt5.QtGui import QKeySequence, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow, QShortcut
from yaml.representer import SafeRepresenter

from autologbook import autoconfig, autoerror, autoprotocol, autotools, autowatchdog
from autologbook.about_dialog_ui import Ui_About
from autologbook.configuration_editor_ui import Ui_configurationDialog
from autologbook.main_window_ui import Ui_MainWindow
from autologbook.mirroring_engine_dialog_ui import Ui_mirroring_engine_dialog
from autologbook.protocol_editor_ui import Ui_tree_viewer_dialog
from autologbook.user_editor_ui import Ui_UserEditor

Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot
urllib3.disable_warnings
represent_literal_str = autotools.change_style(
    '|', SafeRepresenter.represent_str)
yaml.add_representer(autotools.literal_str, represent_literal_str)
log = logging.getLogger('__main__')


class PathValidator():
    """
    Helper class to validate the input paths.

    Use it to validate the input folder fields to decide
    if the watchdog can be started or not.

    """

    Invalid = 0
    AcceptableIfMirroringActive = 10
    AcceptableIfCustomOwnership = 20
    Acceptable = 30

    def __init__(self, path, base_path='R:\\A226\\Results',
                 pattern='^([\\d]+)\\s*[-_]\\s*([\\w\\W]+)\\s*[-_]\\s*([\\w\\W]+)$'):
        r"""
        Build an instance of the PathValidator.

        You won't use it because you should use the static class function ValidatePath

        Note: traditionally Versa paths are starting with a # symbol. While this is perfectly
              ok with the filesystem, when the path is converted to a URI on the image file server
              the # sysmbol is causing problems. The webserver will consider it as the starting
              point of a URL fragment and not part of the URL itself.
              **We cannot accept # symbols in protocol folder on the Image Server!**

        Parameters
        ----------
        path : Path | str
            This is the path that is being validated.
        base_path : Path | str, optional
            This is the base path where all the protocols should be saved.
            The default is 'R:\\A226\\Results'.
        pattern : str, optional
            This is the pattern that the leaf folder should match.
            It should be something like this:
                1234 - ProjectName - ProjectResponsible
            The default is '^([\d]+)\s*[-_]\s*([\w\W]+)\s*[-_]\s*([\w\W]+)$'.

        Returns
        -------
        None.

        """
        self.path = path
        self.base_path = Path(base_path)
        self.pattern = pattern

    def ValidatePath(path, base_path='R:\\A226\\Results',
                     pattern='^*([\\d]+)\\s*[-_]\\s*([\\w\\W]+)\\s*[-_]\\s*([\\w\\W]+)$'):
        """Return the validity of a path."""
        return PathValidator(path, base_path, pattern).validate()

    def getOwnershipParameters(self):
        """
        Retrieve the ownership parameters from the folder name.

        Using the pattern provided in the constructur, try to guess the three
        ownership parameters. If it fails, None is returned.

        Returns
        -------
        int or str
            The project ID
        str
            The project name
        str
            The responsible..

        """
        if self.path == '':
            return None
        self.path = Path(self.path)
        folder_name = self.path.parts[-1]
        match = re.search(self.pattern, folder_name)
        if match:
            return (match[1], match[2], match[3])
        return None

    def validate(self):
        """
        Validate the path.

        This class member can return three possible state:
            1. Invalid. The provided path is invalid and thus the watchdog cannot be start
            2. AcceptableIfMirroringActive. The provided path is not invalid and the watchdog
               can be started if the mirroring is activated and the mirroring folder is Acceptable
            3. Acceptable. The provided path is valid in all cases.

        There are several checks that need to be done:
            1. The path is empty or not existing, or not a directory, then Invalid is returned.
            2. The path is not relative to the base_path, then AcceptableIfMirroringActive is returned.
            3. The path is relative to the base_path, but the leaf directory is not matching the regular
               expression, then AccetableIfMirroringActive is returned.
            4. the path is starting with # symbol (traditional Versa folder), then
               AcceptableIfMirroringActive is returned
            5. The path is relative to the base_path and the leaf directory is matching the regular
               expression then Acceptable is returned.

        Returns
        -------
        VALIDITY Constant
            See the description for an explanation.

        """
        if not self.path:
            return self.Invalid
        self.path = Path(self.path)

        if len(str(self.path)) == 0:
            return self.Invalid
        if self.path.exists() and self.path.is_dir():
            if '#' in str(self.path):
                # found a # symbol in the path. Very likely this is a Versa folder.
                # the folder can be accepted only if it is mirrored somewhere else.
                return self.AcceptableIfMirroringActive
            if self.path.is_relative_to(autoconfig.IMAGE_SERVER_BASE_PATH):
                # the path is in the right position.
                # let's check if the ownership variables are in the folder name
                folder_name = self.path.parts[-1]
                match = re.search(self.pattern, folder_name)
                if match:
                    # very good, we are all set
                    return self.Acceptable
                else:
                    # we need to ask the user to use custom ownership variables
                    return self.AcceptableIfCustomOwnership
            return self.AcceptableIfMirroringActive
        return self.Invalid


class Signaller(QtCore.QObject):
    """
    A sub-class of QObject to contain a signal.

    Only QObejct derived instances are allowed to have a signal, so if you want to have a no
    QtObject to emit a signal, you have to add a Signaller like this to its attributes.

    This specific signaller contains only one Qt Signal emitting a formatted string a logging.LogRecord
    and it is used to establish a communication between a the logging module and a PlainText object in a
    QtWindow.

    """

    signal = Signal(str, logging.LogRecord)


class QtHandler(logging.Handler):
    """
    A sub-class of the logging.Handler.

    It incorporates a Signaller to be able to emit a Qt Signal.

    """

    def __init__(self, slotfunc, *args, **kwargs):
        """
        Build an instance of QtHandler.

        Parameters
        ----------
        slotfunc : CALLABLE
            The slot function which the Signaller.signal is connected.
        *args : positional arguments
            All other positional arguments to be passed to the parent constructor.
        **kwargs : keyword arguments
            All keywork arguments to be passed to the parent constructor.

        Returns
        -------
        None.

        """
        super().__init__(*args, **kwargs)
        self.signaller = Signaller()
        self.signaller.signal.connect(slotfunc)

    def emit(self, record):
        """Emit the signaller signal containing the formatted string and the logging.Record."""
        s = self.format(record)
        self.signaller.signal.emit(s, record)


class Worker(QtCore.QObject):
    """
    A Worker class derived from QObject.

    This class will be performing the real job.
    It will be moved to a separate Thread in order to leave the GUI responsibe

    """

    # signal informing about the worker running status
    worker_is_running = Signal(bool, name='work_is_running')

    def __init__(self, parent=None):
        """
        Build an instance of a generic worker.

        It sets its parent and call the super constructor

        Parameters
        ----------
        parent : Object, optional
            The parent object.

        Returns
        -------
        None.

        """
        self.parent = parent

        # to emulate toggle button
        self.running = False

        # a list with the required parameters
        self.required_parameters = []

        # a dictionary with the actual parameters
        self.params = {}

        super().__init__(parent=parent)

    def updateParameters(self, *args, **kwargs):
        """
        Transfer the execution parameters from the GUI to the worker Thread.

        All keyword arguments are already provided in the code but can be override here

        Keyword arguments
        ------------------

        elog_hostname: STRING
            The FQDN of the elog server including the protocol. For example https://10 .166.16.24

        elog_port: INTEGER
            The numeric value of the port where there elog server is listening.

        elog_user: STRING
            The username connecting to the logbook.

        elog_password: STRING
            The password to connect to the logbook in plain text

        Returns
        -------
        None.

        """
        # check if all required parameters are transmitted
        for param in self.required_parameters:
            if param in kwargs:
                self.params[param] = kwargs[param]
            else:
                log.error('Missing %s. Cannot update woker paramters' % param)
                raise autoerror.MissingWorkerParameter(f'Missing {param}.')


class FSWatchdogWorker(Worker):
    """
    The specialized FSWatchdogWorker.

    It takes care of monitor the FS for changes.
    """

    def __init__(self, parent=None):
        """
        Build an instance of a FSWatchdogWorker.

        Parameters
        ----------
        parent : Object, optional
            The parent object. The default is None.

        Returns
        -------
        None.

        """
        # call the Worker constructor
        super().__init__(parent=parent)

        # this is the reference to the Protocol
        self.autolog = None

        # this is the reference to the Event Handler
        self.autologbookEventHandler = None

        # this is the reference of the observer
        self.observer = None

        # list of required parameters
        self.required_parameters.extend(['path', 'microscope', 'projectID',
                                         'project_name', 'responsible'])

    def updateParameters(self, *args, **kwargs):
        """
        Transfer the execution parameters from the GUI to the FSWatchdogThread.

        Keywords parameters
        -------------------
        path : Path-like or string
            The path being monitored by the FSWatchdogThread

        microscope : string
            The name of the microscope. This will affect the subclass of ELOGProtocol and
            ELOGProtocolEventHandler. Possible values are:
                Quattro : for the Thermofisher Quattro S.
                Versa : for the Thermofisher Versa 3D FIB

        projectID : string or None
            The customized protocol ID. Use None if you want to have it guessed from the
            folder name.

        project_name : string or None
            The project name for the protocol. Use None if you want to have it guessed from the
            folder name.

        responsible : string or None
            The name of the responsible of the experiment. Use None if you want to have it guessed from the
            folder name.

        Those parameters are sent to the worker everytime the enble_watchdog is set,
        and this is happening if and only if the validate_inputs is returning true.

        Returns
        -------
        None.

        """
        # call the super method
        super().updateParameters(*args, **kwargs)

        # now that we have everything, we can create the instances
        if self.params['microscope'] == 'Quattro':
            # create an instance of the QuattroELOGProtocol and assign it to worker
            self.autolog = autoprotocol.QuattroELOGProtocol(
                path=self.params['path'],
                elog_hostname=autoconfig.ELOG_HOSTNAME,
                elog_port=autoconfig.ELOG_PORT,
                elog_user=autoconfig.ELOG_USER,
                elog_password=autoconfig.ELOG_PASSWORD,
                elog_use_ssl=autoconfig.USE_SSL,
                protocol=self.params['projectID'],
                project=self.params['project_name'],
                responsible=self.params['responsible']
            )
            # create an instance of the QuattroELOGProtocolEventHandler
            self.autologbookEventHandler = autowatchdog.QuattroELOGProtocolEventHandler(
                self.autolog)

        elif self.params['microscope'] == 'Versa':
            # create an instance of the VersaELOGProtocol and assign it to worker
            self.autolog = autoprotocol.VersaELOGProtocol(
                path=self.params['path'],
                elog_hostname=autoconfig.ELOG_HOSTNAME,
                elog_port=autoconfig.ELOG_PORT,
                elog_user=autoconfig.ELOG_USER,
                elog_password=autoconfig.ELOG_PASSWORD,
                elog_use_ssl=autoconfig.USE_SSL,
                protocol=self.params['projectID'],
                project=self.params['project_name'],
                responsible=self.params['responsible']
            )
            # create an instance of the VersaELOGProtocolEventHandler
            self.autologbookEventHandler = autowatchdog.VersaELOGProtocolEventHandler(
                self.autolog)

        # connect the autolog.signal_dispatcher to the MainWindow proxy signals
        self.autolog.signal_dispatcher.added_element.connect(
            self.parent.added_element.emit)
        self.autolog.signal_dispatcher.removed_element.connect(
            self.parent.removed_element.emit)

        # reset the HTMLObject
        autoprotocol.HTMLObject.resetHTMLContent()
        # we are ready to start. Just wait the start signal!

    @Slot()
    def start(self):
        """
        Start the FSWatchdogWorker.

        A new Observer instance is generated everytime this slot is called,
        scheduled to work with an autologbookEventHandler and started.

        All the already existing items in the monitored path are also processed.

        IMPORTANT NOTE
        --------------
        Never call this slot directly, but always pass via the toggle slot to
        transform the start watchdog push button in a start/stop toggle switch.

        Returns
        -------
        None.

        """
        # inform the GUI that we have started working
        self.worker_is_running.emit(True)

        # rename the thread
        threading.current_thread().name = autotools.ctname()

        # it's time to have an observer. It is important that a fresh observer is
        # created every time the worker is started, because otherwise the observer
        # won't be able to restart.
        self.observer = watchdog.observers.Observer(
            autoconfig.AUTOLOGBOOK_WATCHDOG_TIMEOUT)
        self.observer.schedule(self.autologbookEventHandler,
                               path=self.params['path'], recursive=True)

        # get a referenceof the observer.event_queue attached to the handler.
        # it is useful for advance operations.
        self.autologbookEventHandler.setQueueReference(
            self.observer.event_queue)
        # Append Obs to the threadname
        self.observer.name = f'{autotools.ctname()}Obs'

        # remember to reset the MicroscopePicture IDs
        autoprotocol.MicroscopePicture._reset_ids()

        # process existing items
        self.autologbookEventHandler.processAlreadyExistingItems()

        # now start to look for new files
        self.observer.start()

    @Slot()
    def stop(self):
        """
        Stop the FSWatchdog.

        A stop signal is sent to the observer so that is not queuing any more
        events.

        The join statement assures that all currently present event in the queue
        are still dispatched.

        The HTML content of the autologbook is generated for the last time and
        since the queue is empty it will also be posted to the ELOG server this
        time with all attachments.

        Finally a signal is sent back to the GUIThread to inform it that the
        watchdog process is finished and the status of the inputs can be changed.

        IMPORTANT NOTE
        --------------
        Never call this slot directly, but always pass via the toggle slot to
        transform the start watchdog push button in a start/stop toggle switch.

        Returns
        -------
        None.

        """
        # stop the observer
        self.observer.stop()

        # wait until the observer is finished
        self.observer.join()

        # for the last time generate the HTML and post it with all the attachments
        autoprotocol.HTMLObject.resetHTMLContent()
        self.autolog.generateHTML()
        self.autolog.postELOGMessage(skipAttachements=False)

        # inform the GUI that we have finished our task.
        self.worker_is_running.emit(False)

    @Slot()
    def toggle(self):
        """
        Toggle the status of the watchdog.

        The watchdog pushbutton on the GUI should have a toggle mechanical
        function instead of a pushbutton one.

        Using this slot we are mimiking the same mechanical behaviour.

        This is actually the only slot that should be connected to the GUIThread
        receiving the start/stop signal.

        Returns
        -------
        None.

        """
        if self.running:
            self.running = False
            self.stop()
        else:
            self.running = True
            self.start()


class FSMirrorWorker(Worker):
    """
    The specialized FSMirrorWorker.

    It takes care of mirroring two directories
    """

    def __init__(self, parent=None):
        """
        Build an instance of a FSMirrorWorker.

        Parameters
        ----------
        parent : Object, optional
            The parent object. The default is None.

        Returns
        -------
        None.

        """
        super().__init__(parent=parent)

        # initializie to None both watchdog relevant variables.
        self.mirroringHandler = None
        self.observer = None

        # initialize the variables for the robocopy
        self.robocopy_process = None

        # list of required parameters
        self.required_parameters.extend(
            ['src_path', 'dst_path', 'is_required', 'engine'])

    def updateParameters(self, *args, **kwargs):
        """
        Transfer the execution parameters from the GUI to the FSMirrorWorkerThread.

        Keywords parameter
        ------------------
        src_path : Path-like or string
            The source path of the mirroring

        dst_path : Path-like or string
            The destination path of the mirroring

        is_required : Bool
            A boolean flag to ask for mirroring or not

        engine : string
            The name of the engine to be used. Available options are:
                watchdog (python filesystem watchdog in a separate thread)
                robocopy (popen thread)
            The watchdog implementation is much faster, but robocopy can be
            more stable in some circumstances.

        Those parameters are sent to the worker everytime the enble_watchdog is set,
        and this is happening if and only if the validate_inputs is returning true

        Returns
        -------
        None.

        """
        super().updateParameters(*args, **kwargs)

        if self.params['engine'] == 'watchdog' and self.params['is_required']:
            self.mirroringHandler = autowatchdog.MirroringHandler(
                self.params['src_path'], self.params['dst_path'])

    @Slot()
    def start(self):
        """
        Start the FSMirrorWorker.

        This slot works differently according to the selected mirroring engine.

        In the case of **watchdog**:

            A new Observer instance is generated everytime this slot is called,
            scheduled to work with a mirroringHandler and started.

            All the already existing items in the monitored path are also processed.

        In the case of **robocopy**:

            robocopy.exe is called via Popen.run to copy all existing items first
            and then started to work as daemon with update time of 1 min.

            While the exit code and eventually the error message of the first
            execution is printed on the logger message, the daemon output is
            saved in a log file in the protocol folder.

        IMPORTANT NOTE
        --------------
        Never call this slot directly, but always pass via the toggle slot to
        transform the start watchdog push button in a start/stop toggle switch.

        Returns
        -------
        None.

        """
        # rename the thread
        threading.current_thread().name = autotools.ctname()
        log.info('Starting mirroring process with %s engine' %
                 self.params['engine'])

        if self.params['engine'] == 'watchdog':

            # it's time to have an observer. It is important that a fresh observer is
            # created every time the worker is started, because otherwise the observer
            # won't be able to restart.
            self.observer = watchdog.observers.Observer(
                timeout=autoconfig.AUTOLOGBOOK_MIRRORING_TIMEOUT)
            self.observer.schedule(self.mirroringHandler,
                                   path=self.params['src_path'], recursive=True)

            # get a referenceof the observer.event_queue attached to the handler.
            # it is useful for advance operations.
            self.mirroringHandler.setQueueReference(self.observer.event_queue)
            # Append Obs to the threadname
            self.observer.name = f'{autotools.ctname()}Obs'

            # process existing items
            self.mirroringHandler.process_all_existing()

            # now start to look for new files
            self.observer.start()

        elif self.params['engine'] == 'robocopy':
            log.warning(
                'Robocopy cannot remove extra images from the destination folder.')
            log.warning(
                'If you delete a file in the src folder, you need to remove it *MANUALLY* from the destination.')
            log.warning(
                'Use watchdog engine (-m watchdog) to avoid this issue.')

            # first copy all existing file and wait for completition
            options = ['/s']
            commandlist = [autoconfig.ROBOCOPY_EXE,
                           str(self.params['src_path']), str(self.params['dst_path'])]
            commandlist.extend(options)
            preMirroringProcess = subprocess.run(
                commandlist, shell=False, capture_output=True)
            if preMirroringProcess.returncode == 16:
                log.error(autotools.decodeCommandOutput(
                    preMirroringProcess.stdout))
                log.error(autotools.decodeCommandOutput(
                    preMirroringProcess.stderr))
            else:
                log.info('Mirroring all existing files and folders successfully')

            # now start the monitoring task
            now = datetime.now()
            logfile = '{}-robocopy.log'.format(now.strftime('%Y%m%d-%H%M%S'))
            options = ['*.tif*', '*.j*pg', '*.y*ml', '*.pdf', '*.txt', '*.log',
                       '/lev:1', '/LOG:{}'.format(self.params['src_path'] / logfile), '/E', '/MON:1']
            commandlist = [autoconfig.ROBOCOPY_EXE,
                           str(self.params['src_path']), str(self.params['dst_path'])]
            commandlist.extend(options)
            self.robocopy_process = subprocess.Popen(
                commandlist, shell=False, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

            log.info('Robocopy process with PID %s is running' %
                     self.robocopy_process.pid)

    @Slot()
    def toggle(self):
        """
        Toggle the status of the mirroring watchdog.

        The watchdog pushbutton on the GUI should have a toggle mechanical
        function instead of a pushbutton one.

        Using this slot we are mimiking the same mechanical behaviour.

        This is actually the only slot that should be connected to the GUIThread
        receiving the start/stop signal.

        Returns
        -------
        None.

        """
        if self.params['is_required']:
            if self.running:
                self.running = False
                self.stop()
            else:
                self.running = True
                self.start()

    @Slot()
    def stop(self):
        """
        Stop the FSMirroringWatchdog.

        This slot behaves in different way depending on the mirroring engine.

        In the case of **watchdog**:

        A stop signal is sent to the observer so that is not queuing any more
        events.

        The join statement assures that all currently present event in the queue
        are still dispatched.

        In the case of **robocopy**:

        The daemon instance of robocopy is killed and then a last copy of the
        eventually remaining files to be copied is done. This is due to the fact
        that up to a minute can be passed since the last time the daemon was
        copying the files.

        It must be noted that those last copied files may not be processed by
        the AutologEventHandler because its observer could be already stopped
        by then. This is a know limitation of the robocopy engine.

        IMPORTANT NOTE
        --------------
        Never call this slot directly, but always pass via the toggle slot to
        transform the start watchdog push button in a start/stop toggle switch.

        Returns
        -------
        None.

        """
        log.info('Stopping mirroring process with %s engine' %
                 self.params['engine'])
        if self.params['engine'] == 'watchdog':
            # stop the observer
            self.observer.stop()

            # wait until the observer is finished
            self.observer.join()
        elif self.params['engine'] == 'robocopy':
            self.robocopy_process.kill()
            log.info('Stopped robocopy process with PID %s',
                     self.robocopy_process.pid)

            # robocopy is executed only once per minute. it is possible that when
            # we kill it there were other files to be copied.
            # just copy everything new again
            options = ['*.tif*', '*.j*pg',
                       '*.y*mlepdf', '*.txt', '*.log', '/s']
            commandlist = [autoconfig.ROBOCOPY_EXE,
                           str(self.params['src_path']), str(self.params['dst_path'])]
            commandlist.extend(options)
            preMirroringProcess = subprocess.run(
                commandlist, shell=False, capture_output=True)
            if preMirroringProcess.returncode == 16:
                log.error(autotools.decodeCommandOutput(
                    preMirroringProcess.stdout))
                log.error(autotools.decodeCommandOutput(
                    preMirroringProcess.stderr))
            else:
                log.info('Mirroring all remaining files successfully')


class AboutDialog(QDialog, Ui_About):
    """
    About Autologog Dialog.

    A very simple dialog message without button to show information about this
    program.
    """

    def __init__(self, parent=None):
        """
        Build an instance of the AboutDialog.

        Parameters
        ----------
        parent : QtObject, optional
            The parent calling QtObject. The default is None.

        Returns
        -------
        None.

        """
        super().__init__()
        self.setupUi(self)


class MirroringEngineDiaolog(QDialog, Ui_mirroring_engine_dialog):
    """
    A simple dialog for the selection of the mirroring engine.

    This is a simplified configuration editor dialog that is just used in case
    you need to quickly change the mirroring engine.

    """

    def __init__(self, parent=None):
        """
        Build an instance of the MirroringEngineDialog.

        Parameters
        ----------
        parent : QtObject, optional
            The parent caller of this dialog. The default is None.

        Returns
        -------
        None.

        """
        super().__init__()
        self.setupUi(self)


class ConfigurationEditorDialog(QDialog, Ui_configurationDialog):
    """
    A complete configuration editor dialog.

    This dialog window allows the user to manipulate all configuration
    parameters.

    The user can load a file, save the current configuration to a file or
    reset to the default configuration.

    """

    def __init__(self, parent=None):
        """
        Build an instance of the ConfigurationEditorDialog.

        Parameters
        ----------
        parent : QtObject, optional
            The parent caller of this dialog. The default is None.

        Returns
        -------
        None.

        """
        super().__init__()
        self.setupUi(self)

        # use this boolean to check if the password was changed during the
        # configuration editing.
        self.password_changed = False

        # use this string to store the encrypted password
        self.encrypted_pwd = ''

    @Slot(str)
    def password_edited(self, newPlainTextPWD):
        """
        React to a password change.

        When the user edits the password, he is introducing a plain text string.
        This will never be save in the configuration file nor in the configuration
        object.

        This slot is automatically invoked whenever the password field is edited,
        the new encrypted password is calculated and a flag to signalize that the
        password must be updated is raised.

        Parameters
        ----------
        newPlainTextPWD : string
            The new plain text password.

        Returns
        -------
        None.

        """
        self.password_changed = True
        self.encrypted_pwd = autotools.encrypt_pass(newPlainTextPWD)

    def setAllValues(self, config):
        """
        Set the values of all widtges to what is stored in the configuration object.

        The coding style of this method is terrible, I will look for something
        better.

        Parameters
        ----------
        config : ConfigParser object
            The configuration parser object containing all the paramters.

        Returns
        -------
        None.

        """
        # elog
        self.elog_user_field.setText(config['elog'].get('elog_user'))
        self.elog_password_field.setText(config['elog'].get('elog_password'))
        self.elog_hostname_field.setText(config['elog'].get('elog_hostname'))
        self.elog_port_field.setValue(int(config['elog'].get('elog_port')))
        self.elog_max_auth_error_field.setValue(
            int(config['elog'].get('max_auth_error')))
        self.elog_ssl_check_box.setChecked(
            config.getboolean('elog', 'use_ssl'))
        # autolog
        self.autologbook_max_attempts_spinbox.setValue(
            int(config['Autologbook watchdog'].get('max_attempts')))
        self.autologbook_wait_min_spinbox.setValue(
            float(config['Autologbook watchdog'].get('wait_min')))
        self.autologbook_wait_max_spinbox.setValue(
            float(config['Autologbook watchdog'].get('wait_max')))
        self.autologbook_wait_increment_spinbox.setValue(
            float(config['Autologbook watchdog'].get('wait_increment')))
        self.autologbook_min_delay_spinbox.setValue(
            float(config['Autologbook watchdog'].get('minimum delay between elog post')))
        self.autologbook_observer_timeout_spinbox.setValue(
            config.getfloat('Autologbook watchdog', 'observer_timeout'))
        # mirroring
        self.engine_combobox.setCurrentText(
            config['Mirroring engine'].get('engine'))
        self.mirroring_max_attempts_spinbox.setValue(
            int(config['Mirroring watchdog'].get('max_attempts')))
        self.mirroring_wait_spinbox.setValue(
            float(config['Mirroring watchdog'].get('wait')))
        self.mirroring_observer_timeout_spinbox.setValue(
            config.getfloat('Mirroring watchdog', 'observer_timeout'))
        # external
        self.notepad_field.setText(
            config['external tools'].get('favourite text editor'))
        self.robocopy_field.setText(config['external tools'].get('robocopy'))
        # quattro
        self.quattro_elog_logbook_field.setText(
            config['Quattro'].get('logbook'))
        self.quattro_navcam_size_spinbox.setValue(
            int(config['Quattro'].get('image_navcam_width')))
        # versa
        self.versa_elog_logbook_field.setText(
            config['Versa'].get('logbook'))
        # image server
        self.base_path_field.setText(config['Image_server'].get('base_path'))
        self.server_root_field.setText(
            config['Image_server'].get('server_root'))
        self.img_thumb_size_spinbox.setValue(
            int(config['Image_server'].get('image_thumb_width')))
        self.custom_id_start_spinBox.setValue(
            config.getint('Image_server', 'custom_id_start'))
        self.custom_id_tiff_tag_spinBok.setValue(
            config.getint('Image_server', 'tiff_tag_code'))

        # be sure that the software is informed that the password has not been
        # changed yet.
        self.password_changed = False

    def get_conf(self):
        """
        Get a configuration object from the value in the dialog.

        A configuration parser object is created with all the sections and all
        the options set to the values in the dialog.

        Returns
        -------
        config : ConfigParser
            A ConfigParser containing the options contained in the dialog.

        """
        config = configparser.ConfigParser()
        if self.password_changed:
            new_password = self.encrypted_pwd
        else:
            new_password = self.elog_password_field.text()
        config['elog'] = {
            'elog_user': self.elog_user_field.text(),
            'elog_password': new_password,
            'elog_hostname': self.elog_hostname_field.text(),
            'elog_port': str(self.elog_port_field.value()),
            'use_encrypt_pwd': True,
            'max_auth_error': self.elog_max_auth_error_field.value(),
            'use_ssl': self.elog_ssl_check_box.isChecked(),
            '; To manually insert a (plain text) password, set use_encrypt_pwd to False.': ''
        }
        config['Autologbook watchdog'] = {
            'max_attempts': str(self.autologbook_max_attempts_spinbox.value()),
            'wait_min': str(self.autologbook_wait_min_spinbox.value()),
            'wait_max': str(self.autologbook_wait_max_spinbox.value()),
            'wait_increment': str(self.autologbook_wait_increment_spinbox.value()),
            'minimum delay between elog post': str(self.autologbook_min_delay_spinbox.value()),
            'observer_timeout': self.autologbook_observer_timeout_spinbox.value()
        }
        config['Mirroring engine'] = {
            'engine': self.engine_combobox.currentText()
        }
        config['Mirroring watchdog'] = {
            'max_attempts': str(self.mirroring_max_attempts_spinbox.value()),
            'wait': str(self.mirroring_wait_spinbox.value()),
            'observer_timeout': self.mirroring_observer_timeout_spinbox.value()
        }
        config['external tools'] = {
            'favourite text editor': str(Path(self.notepad_field.text())),
            'robocopy': str(Path(self.robocopy_field.text()))
        }
        config['Quattro'] = {
            'logbook': self.quattro_elog_logbook_field.text(),
            'image_navcam_width': self.quattro_navcam_size_spinbox.value()
        }
        config['Versa'] = {
            'logbook': self.versa_elog_logbook_field.text()
        }
        config['Image_server'] = {
            'base_path': str(Path(self.base_path_field.text())),
            'server_root': self.server_root_field.text(),
            'image_thumb_width': self.img_thumb_size_spinbox.value(),
            'custom_id_start': self.custom_id_start_spinBox.value(),
            'tiff_tag_code': self.custom_id_tiff_tag_spinBok.value()
        }
        self.password_changed = False
        return config

    @Slot()
    def save_conf_file(self):
        """
        Save the configuration from the dialog to a file.

        This slot is connected with Save configuration push button.

        Returns
        -------
        None.

        """
        directory = Path.home() / Path('Documents')
        conffile = QFileDialog.getSaveFileName(self, 'Save configuration file', directory=str(directory),
                                               filter='Configuration file (*.ini)')
        if conffile[0]:
            conf = self.get_conf()
            with open(conffile[0], 'w') as f:
                conf.write(f)

    @Slot()
    def load_conf_file(self):
        """
        Load a configuration file to the dialog.

        This slot is connected to the load file pushbutton.

        Returns
        -------
        None.

        """
        directory = Path.home() / Path('Documents')
        conffile = QFileDialog.getOpenFileName(self, 'Open configuration file', directory=str(directory),
                                               filter='Configuration file (*.ini)')
        if conffile[0]:
            conf = configparser.ConfigParser()
            conf = autotools.safe_configread(conffile[0])
            self.setAllValues(conf)

    @Slot()
    def reset_conf(self):
        """
        Reset the content of the dialog to the default.

        This slot is connected to the reset default pushbutton.

        Returns
        -------
        None.

        """
        self.setAllValues(autotools.generate_default_conf())

    @Slot()
    def search_text_editor(self):
        """
        Search for a text editor.

        The preferred editor is notepad++ but it is generally not in the path
        so that the which command cannot find.

        A QFileDialog is opened in the program file folder for the user to
        search for a text editor.

        This slot is connected to the tool button next to the text editor input.

        Returns
        -------
        None.

        """
        directory = shutil.which('notepad++.exe')
        if not directory:
            directory = os.environ['ProgramFiles']
        file = QFileDialog.getOpenFileName(self, 'Text editor executable', directory=str(directory),
                                           filter='Executable (*.exe)')
        if file[0]:
            self.notepad_field.setText(str(Path(file[0])))

    @Slot()
    def search_robocopy(self):
        """
        Search for robocopy.

        Robocopy is generally installed on Windows system and searchable in the
        path with the which command.

        A QFileDialog is opened with the result of the which command or in the
        ProgramFiles folder for the user to select robocopy.exe.

        This slot is connected to the tool button next to the robocopy input.

        Returns
        -------
        None.

        """
        directory = shutil.which('robocopy.exe')
        if not directory:
            directory = os.environ['ProgramFiles']
        file = QFileDialog.getOpenFileName(self, 'Robocopy executable', directory=str(directory),
                                           filter='Executable (*.exe)')
        if file[0]:
            self.robocopy_field.setText(str(Path(file[0])))

    @Slot()
    def search_basepath(self):
        """
        Search for the base path of the image server.

        This slot is connected to the tool button next to base folder input.

        Returns
        -------
        None.

        """
        if self.base_path_field:
            directory = Path(self.base_path_field.text())
        else:
            directory = Path.home() / Path('Documents')
        returnpath = QFileDialog.getExistingDirectory(self, 'Select base path of image server',
                                                      directory=str(directory))
        if returnpath:
            self.base_path_field.setText(returnpath)


item_type = QtCore.Qt.UserRole + 1
description_role = QtCore.Qt.UserRole + 2
extra_role = QtCore.Qt.UserRole + 3
image_role = QtCore.Qt.UserRole + 4
pic_id_role = QtCore.Qt.UserRole + 10
caption_role = QtCore.Qt.UserRole + 11
description_role = QtCore.Qt.UserRole + 12
extra_role = QtCore.Qt.UserRole + 13


class TextItem(QStandardItem):
    """Text item derived from QStandardItem."""

    def __init__(self, txt=''):
        """
        Construct a new TextItem.

        The item_type role is set to Text.

        Parameters
        ----------
        txt : str, optional
            This is the text used as a display role. The default is ''.

        Returns
        -------
        None.
        """
        super().__init__()
        self.setText(txt)
        self.setData('Text', item_type)


class SectionItem(TextItem):
    """
    Section item derived from TextItem.

    This item is used to store section information.

    """

    def __init__(self, txt=''):
        """
        Construct a new SectionItem.

        The item_type role is set to Section.

        Parameters
        ----------
        txt : str, optional
            This is the text used as a display role. The default is ''.

        Returns
        -------
        None.

        """
        super().__init__(txt=txt)
        self.setData('Section', item_type)

    def getDataFromYAML(self, yamlDict):
        """
        Retrieve the item information already stored in the YAML dictionary.

        Parameters
        ----------
        yamlDict : Dictionary
            YAML Dictionary where the information of the Item are stored.

        Returns
        -------
        None.

        """
        key = self.text()
        if key in yamlDict.keys():
            if 'Description' in yamlDict[key].keys():
                self.setData(yamlDict[key]['Description'], description_role)
            if 'Extra' in yamlDict[key].keys():
                self.setData(yamlDict[key]['Extra'], extra_role)


class NavPicItem(TextItem):
    """
    Navigation Picture Item.

    This type is used to store navigation images.
    """

    def __init__(self, txt='', img_link=''):
        """
        Constructur an instance of NaPicItem.

        The type of this item is set to NavPic.

        Parameters
        ----------
        txt : str, optional
            The name of the picture used as display_role. The default is ''.
        img_link : str, optional
            The URL where the thumbnail of the image. The default is ''.

        Returns
        -------
        None.

        """
        super().__init__(txt=txt)
        self.setData('NavPic', item_type)
        self.setData(img_link, image_role)

    def getDataFromYAML(self, yamlDict):
        """
        Retrieve the item information already stored in the YAML dictionary.

        Parameters
        ----------
        yamlDict : Dictionary
            YAML Dictionary where the information of the Item are stored.

        Returns
        -------
        None.

        """
        key = self.text()
        if key in yamlDict.keys():
            if 'Caption' in yamlDict[key].keys():
                self.setData(yamlDict[key]['Caption'], caption_role)
            if 'Description' in yamlDict[key].keys():
                self.setData(yamlDict[key]['Description'], description_role)
            if 'Extra' in yamlDict[key].keys():
                self.setData(yamlDict[key]['Extra'], extra_role)


class MicroPicItem(TextItem):
    """
    Microscope Picture Item.

    This type is used to store microscope pictures.
    """

    def __init__(self, txt='', img_id=0, img_link=''):
        """
        Constructur an instance of MicroPicItem.

        The type of this item is set to MicroPic.

        Parameters
        ----------
        img_id : int, optional
            The identification number of the microscope image. The default is 0.

        img_link : str, optional
            The URL where the thumbnail of the image. The default is ''.

        Returns
        -------
        None.

        """
        super().__init__(txt=txt)
        self.setData('MicroPic', item_type)
        self.setData(img_id, pic_id_role)
        self.setData(img_link, image_role)

    def getDataFromYAML(self, yamlDict):
        """
        Retrieve the item information already stored in the YAML dictionary.

        Parameters
        ----------
        yamlDict : Dictionary
            YAML Dictionary where the information of the Item are stored.

        Returns
        -------
        None.

        """
        pic_id = int(self.data(pic_id_role))
        if pic_id in yamlDict.keys():
            pass
        elif int(pic_id) in yamlDict.keys():
            pic_id = int(pic_id)
        else:
            return
        if 'Caption' in yamlDict[pic_id].keys():
            self.setData(yamlDict[pic_id]['Caption'], caption_role)
        if 'Description' in yamlDict[pic_id].keys():
            self.setData(yamlDict[pic_id]['Description'], description_role)
        if 'Extra' in yamlDict[pic_id].keys():
            self.setData(yamlDict[pic_id]['Extra'], extra_role)


class UserEditor(QDialog, Ui_UserEditor):
    """Dialog window for the user credential editor."""

    def __init__(self, parent=None, username=None, password=None):
        """
        Build a new instance of the user editor.

        Parameters
        ----------
        parent : QObject, optional
            The parent object, very likely the MainWindow. The default is None.
        username : string, optional
            The current user name. The default is None
        password : string, optional
            The current password. The default is None

        Returns
        -------
        None.

        """
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.username = username
        self.username_line_edit.setText(username)
        self.password = password
        self.password_line_edit.setText(password)

    @Slot(str)
    def password_edited(self, newPlainTextPWD):
        """
        React to a passward change.

        This slot is called everytime the password field is edited.

        Parameters
        ----------
        newPlainTextPWD : string
            The newply entered passowrd in plain text.

        Returns
        -------
        None.

        """
        self.password = autotools.encrypt_pass(newPlainTextPWD)

    @Slot(str)
    def username_edited(self, newUsername):
        """
        React to a username change.

        This slot is called everytime the username field is edited.

        Parameters
        ----------
        newUsername : string
            The newply entered username in plain text.

        Returns
        -------
        None.

        """
        self.username = newUsername


class ProtocolEditor(QDialog, Ui_tree_viewer_dialog):
    """Dialog window for the protocol editor."""

    def __init__(self, parent=None, autolog=None):
        """
        Build a new instance of the protocol editor.

        Parameters
        ----------
        parent : QObject, optional
            The parent object, very likely the MainWindow. The default is None.
        autolog : autologbook.Protocol, optional
            An instance of the protocol. The default is None.

        Returns
        -------
        None.

        """
        super().__init__(parent)
        self.parent = parent
        self.autolog = autolog
        self.setupUi(self)

        # set up the shortcut to update the model-
        self.update_shortcut = QShortcut((QKeySequence('Ctrl+S')), self)
        self.update_shortcut.activated.connect(self.update_protocol)

        # connect the signals from MainWindow
        self.parent.added_element.connect(self.add_element)
        self.parent.removed_element.connect(self.remove_element)
        self.parent.change_autolog.connect(self.change_autolog)

        self.autolog_tree_viewer.setHeaderHidden(True)

        # generate the model
        self.treeModel = QStandardItemModel()
        self.rootNode = self.treeModel.invisibleRootItem()
        self.generate_model()
        self.autolog_tree_viewer.setModel(self.treeModel)
        self.autolog_tree_viewer.expandAll()

        self.autolog_tree_viewer.selectionModel(
        ).selectionChanged.connect(self.get_and_update_values)
        self.treeModel.rowsInserted.connect(
            lambda: self.autolog_tree_viewer.expandAll())

    @Slot(autoprotocol.Protocol)
    def change_autolog(self, autolog):
        """
        Change the reference to the autolog.

        Parameters
        ----------
        autolog : autoprotocol.Protocol
            The reference of the current autolog.

        Returns
        -------
        None.

        """
        log.debug('Changing the autolog reference')
        self.autolog = autolog
        self.refresh_view()

    def refresh_view(self):
        """
        Regenerate the content of the TreeModel.

        This function is used to assure that the model content is update and
        what is shown in the editor window corresponds to the protocol model.

        Returns
        -------
        None.

        """
        self.treeModel.removeRows(0, self.treeModel.rowCount())
        self.generate_model()

    def generate_model(self):
        """
        Generate the data model.

        We use a QStandardItemModel.

        This method generates the whole model standard from the autolog instance

        Returns
        -------
        None.

        """
        introduction_section = SectionItem('Introduction')
        introduction_section.getDataFromYAML(self.autolog.yamlDict)
        self.rootNode.appendRow(introduction_section)

        # a navigation camera section exists only if the protocol is of a
        # Quattro microscope.
        if isinstance(self.autolog, autoprotocol.QuattroELOGProtocol):
            navcam_section = SectionItem('Navigation images')
            navcam_section.getDataFromYAML(self.autolog.yamlDict)

            for navpic in self.autolog.navcamimages:
                navpic_item = NavPicItem(Path(navpic).name, str(Path(navpic)))
                navpic_item.getDataFromYAML(self.autolog.yamlDict)
                navcam_section.appendRow(navpic_item)

            self.rootNode.appendRow(navcam_section)

        sample_section = SectionItem('Samples')
        sample_section.getDataFromYAML(self.autolog.yamlDict)

        for name, sample in self.autolog.samples.items():
            if sample.parent is None:
                log.debug('Adding top level sample %s' % name)
                # we got a top level sample. add this and process
                # all its child
                entry = SectionItem(txt=sample.name)
                for key, image in sample.images.items():
                    pic = MicroPicItem(
                        Path(key).name, image.getID(), image.thumbfilename)
                    pic.getDataFromYAML(self.autolog.yamlDict)
                    entry.appendRow(pic)
                if len(sample.subsamples) != 0:
                    self.addSubSampleRecursively(sample.subsamples, entry)
                sample_section.appendRow(entry)

        self.rootNode.appendRow(sample_section)

        conclusion_section = SectionItem('Conclusion')
        conclusion_section.getDataFromYAML(self.autolog.yamlDict)
        self.rootNode.appendRow(conclusion_section)

    def addSubSampleRecursively(self, sample_list, parent_entry):
        """
        Add a subsample list to a parent sample resursively.

        When building the protocol model, all subsample of a parent must be
        registered and this procedure must be repeated recursively.

        Parameters
        ----------
        sample_list : list
            The list of subsamples belonging to the parent sample.
        parent_entry : SectionItem
            The section item where the subsamples must be appended.

        Returns
        -------
        None.

        """
        for sample_name in sample_list:
            if sample_name in self.autolog.samples.keys():
                sample = self.autolog.samples[sample_name]
                log.debug('Adding subsample %s to %s' %
                          (sample_name, sample.parent))
                entry = SectionItem(txt=sample_name)
                for key, image in sample.images.items():
                    pic = MicroPicItem(
                        Path(key).name, image.getID(), image.thumbfilename)
                    pic.getDataFromYAML(self.autolog.yamlDict)
                    entry.appendRow(pic)
            if len(sample.subsamples) != 0:
                self.addSubSampleRecursively(sample.subsamples, entry)
            parent_entry.appendRow(entry)

    @Slot(str, str, str)
    def add_element(self, element_type, element_name, parent_name):
        """
        Add an element to the model.

        Slot function connected to the addition of a new element to the model

        Parameters
        ----------
        element_type : string
            Possibile element_types are:
                - 'NavPic' : Navigation picture
                - 'MicroPic' : Microscope picture
                - 'Sample': a new sample
        element_name : string
            For NavPic and MicroPic the element name is the full path of the
            image.
            For Sample, it is just the sample name
        parent_name : string
            For MicroPic, the sample name.
            For Sample, the parent name or 'Samples' for top level samples.

        Raises
        ------
        ValueError
            Raised if more than one parent section is found in the model


        Returns
        -------
        None.

        """
        if element_type == 'NavPic':
            # element_name must be the full path
            path = Path(element_name)
            name = path.name

            # the parent name must be Navigation images
            items = self.treeModel.findItems(
                'Navigation images', QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
            if len(items) == 1:
                new_item = NavPicItem(name, str(path))
                new_item.getDataFromYAML(self.autolog.yamlDict)
                items[0].appendRow(new_item)
            else:
                raise ValueError(
                    'More than one navigation image section found')
        elif element_type == 'MicroPic':
            # element_name must be the full path
            path = Path(element_name)
            name = path.name
            sample = parent_name
            image = self.autolog.samples[sample].images[str(path)]
            image_id = image.getID()
            thumb = image.thumbfilename

            pic = MicroPicItem(name, image_id, thumb)
            pic.getDataFromYAML(self.autolog.yamlDict)

            items = self.treeModel.findItems(
                sample, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
            if len(items) == 1:
                items[0].appendRow(pic)
            else:
                raise ValueError(
                    f'More than one sample {sample} in the protocol.')
        elif element_type == 'Sample':
            # the parent name must be Samples
            new_sample = SectionItem(element_name)
            items = self.treeModel.findItems(
                parent_name, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
            if len(items) == 1:
                items[0].appendRow(new_sample)
            else:
                raise ValueError('More than one samples section')

    @Slot(str, str, str)
    def remove_element(self, element_type, element_name, parent_name):
        """
        Remove an element from the model.

        Slot function connected to the removal of an existing element to the model

        Parameters
        ----------
        element_type : string
            Possibile element_types are:
                - 'NavPic' : Navigation picture
                - 'MicroPic' : Microscope picture
                - 'Sample': a new sample
        element_name : string
            For NavPic and MicroPic the element name is the full path of the
            image.
            For Sample, it is just the sample name
        parent_name : string
            For MicroPic, the sample name.
            Useless for NavPic and Sample.

        Returns
        -------
        None.

        """
        if element_type in ('NavPic', 'MicroPic'):
            name = Path(element_name).name
        elif element_type == 'Sample':
            name = element_name

        items = self.treeModel.findItems(
            name, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
        if len(items) == 1:
            item = items[0]
            parent_index = item.parent().index()
            item.model().removeRow(item.row(), parent_index)
        elif len(items) > 1:
            log.error('Expected only one element with name %s.' % name)
            log.error('Found instead %s' % len(items))
            log.warning('Removing all of them and verify the protocol.')
            for item in items:
                if item.parent().text() == parent_name:
                    parent_index = item.parent().index()
                    item.model().removeRow(item.row(), parent_index)

    @Slot(QItemSelection, QItemSelection)
    def get_and_update_values(self, newItem, oldItem):
        """
        Get the new item and save the old one.

        This slot is called everytime the selection of the treeview is changed.
        The oldItem was the one previously selected, for this item we need to
        save the information inserted by the user in the text edit fields.
        This is accomplished by the update_values method

        The newItem is the currntly selected line. For this we need to retrieve
        the information and show them in the text edit fields.
        This is accomplished by the get_values method.


        Parameters
        ----------
        newItem : QItemSelection
            The list of items currently selected.
        oldItem : TYPE
            The list of items that were previosly selected.

        Returns
        -------
        None.

        """
        if oldItem:
            oldIndex = oldItem.indexes()[0]
            self.update_values(oldIndex)
        if newItem:
            # self.autolog_tree_viewer.model().indexFromItem(newItem)
            newIndex = newItem.indexes()[0]
            self.get_values(newIndex)

    def update_values(self, index):
        """
        Update the values of the item corresponding to index.

        The information contained in the edit fields are transferred to the
        data container of the Item and also to the autolog yamlDict.
        In this way, the next time the autologbook triggers a regenaration of
        the HTML, the new information saved in the yamlDict are applied.

        Parameters
        ----------
        index : QModelIndex
            The index of the item to be updated.

        Returns
        -------
        None.

        """
        key = ''
        if index.data(item_type) == 'MicroPic':
            key = int(index.data(pic_id_role))
        else:
            key = index.data()

        if index.data(item_type) in ('NavPic', 'MicroPic'):
            if key not in self.autolog.yamlDict.keys():
                self.autolog.yamlDict[key] = {
                    'Caption': '', 'Description': '', 'Extra': ''}
            if self.caption_field.text():
                self.autolog.yamlDict[key]['Caption'] = self.caption_field.text(
                )
            index.model().setData(index, self.caption_field.text(), caption_role)
        else:
            if key not in self.autolog.yamlDict.keys():
                self.autolog.yamlDict[key] = {'Description': '', 'Extra': ''}

        self.autolog.yamlDict[key]['Description'] = autotools.literal_str(
            self.description_input.document().toPlainText())
        index.model().setData(
            index, self.description_input.document().toPlainText(), description_role)

        self.autolog.yamlDict[key]['Extra'] = autotools.literal_str(
            self.extrainfo_input.document().toPlainText())
        index.model().setData(index, self.extrainfo_input.document().toPlainText(), extra_role)

    @Slot(QModelIndex)
    def get_values(self, index):
        """
        Retrieve the data from the item and display them.

        Parameters
        ----------
        index : QModelIndex
            The index corresponding to the item being displayed.

        Returns
        -------
        None.

        """
        if index.data(item_type) == 'NavPic':
            self.image_preview.setPixmap(
                QPixmap(index.data(image_role)).scaledToWidth(390, 1))
            self.caption_field.setEnabled(True)
            self.caption_field.setText(index.data(caption_role))
            self.description_input.setPlainText(index.data(description_role))
            self.extrainfo_input.setPlainText(index.data(extra_role))
        elif index.data(item_type) == 'MicroPic':
            self.image_preview.setPixmap(
                QPixmap(index.data(image_role)).scaledToWidth(390, 1))
            self.caption_field.setEnabled(True)
            self.caption_field.setText(index.data(caption_role))
            self.description_input.setPlainText(index.data(description_role))
            self.extrainfo_input.setPlainText(index.data(extra_role))
        elif index.data(item_type) == 'Text':
            self.image_preview.setText(
                'Image preview not available for this element')
            self.caption_field.clear()
            self.caption_field.setEnabled(False)
            self.description_input.setPlainText(index.data(description_role))
            self.extrainfo_input.setPlainText(index.data(extra_role))
        elif index.data(item_type) == 'Section':
            self.image_preview.setText(
                'Image preview not available for this element')
            self.caption_field.clear()
            self.caption_field.setEnabled(False)
            self.description_input.setPlainText(index.data(description_role))
            self.extrainfo_input.setPlainText(index.data(extra_role))

    @Slot()
    def update_protocol(self):
        """
        Update the protocol.

        Slot connected to the Update protocol. When clicked the current item values
        are transferred to the yamlDict and the whole yamlDict is dumped to the
        yaml protocol file.

        This filesystem change triggers the watchdog to force the generation of
        the whole HTML and its pubblication to the ELOG.

        Returns
        -------
        None.

        """
        if self.autolog_tree_viewer.selectionModel().currentIndex().isValid():
            self.update_values(
                self.autolog_tree_viewer.selectionModel().currentIndex())
        with open(self.autolog.yamlFilename, 'w', encoding='utf-8') as f:
            yaml.dump(self.autolog.yamlDict, f, allow_unicode=True)


class MainWindow(QMainWindow, Ui_MainWindow):
    """The main window of the GUI."""

    # Used to have different colors for each logging level.
    COLORS = {
        logging.DEBUG: 'black',
        logging.INFO: 'blue',
        logging.WARNING: 'orange',
        logging.ERROR: 'red',
        logging.CRITICAL: 'purple'
    }

    # prepare custom signals
    added_element = Signal(str, str, str, name='added_element')
    removed_element = Signal(str, str, str, name='removed_element')
    change_autolog = Signal(autoprotocol.Protocol, name='change_autolog')

    def __init__(self, app, config):
        """
        Build an instance of the GUI main window.

        Setup the user interface as produced by the QtDesigner
        Setup the logging machinery in order to have all logging messages
        redirected to the GUI
        Call the start_thread method and finally do all signal slot connections.

        Parameters
        ----------
        app : QApplication
            The application calling the main window.

        Returns
        -------
        None.

        """
        super().__init__()
        self.app = app
        self.config = config
        self.setupUi(self)

        # set the protocol editor to none
        self.protocol_editor = None

        # create a logging handler with a slot function pointing to update_status
        self.handler = QtHandler(self.update_status)

        # create a formatter and assign it to the handler
        fs = '[%(asctime)s] %(threadName)-15s %(levelname)-8s %(message)s'
        formatter = logging.Formatter(fs, datefmt='%Y%m%d-%H:%M:%S')
        self.handler.setFormatter(formatter)
        log.addHandler(self.handler)

        # initialize workers and threads dictionaries
        self.workers = {}
        self.worker_threads = {}

        # start the threads and their workers
        self.start_thread()

        self.base_path = Path(autoconfig.IMAGE_SERVER_BASE_PATH)
        self.pattern = '^#*([\\d]+)\\s*[-_]\\s*([\\w\\W]+)\\s*[-_]\\s*([\\w\\W]+)$'
        self.is_watchdog_running = False
        self.is_watchdog_enabled = False

        self.is_ok_to_start = False
        self.are_user_credentials_checked = False
        self.is_mirroring_requested = self.mirror_checkBox.isChecked()
        self.is_custom_ownership_requested = self.custom_ownership_checkbox.isChecked()
        self.protocol_folder_path = None
        self.mirroring_folder_path = None
        self.microscope = 'Quattro'
        self.connectSignalsSlot()

    def show(self):
        """
        Show the main windown.

        Overload of the parent show method adding a message in the log window
        """
        log.info('Welcome to the autologbook GUI!')
        super().show()

    def start_thread(self):
        """
        Start all the needed threads.

        The program is using a separate thread for each of the three workers plus
        another one executing the GUI.

        A reference of all workers and threads are stored in the self.workers
        and self.worker_threads dictionaries.

        Returns
        -------
        None.

        """
        worker_list = {
            'FSWatchdog': {
                'WorkerClassType': 'FSWatchdogWorker',
                'WorkerObjectName': 'FSWatchdog',
                'WorkerThreadName': 'AutoThread'
            },
            'FSMirror': {
                'WorkerClassType': 'FSMirrorWorker',
                'WorkerObjectName': 'Mirror',
                'WorkerThreadName': 'MirrorThread'

            }
        }
        for key, worker in worker_list.items():
            new_worker = globals()[worker['WorkerClassType']]()
            new_worker.parent = self
            new_worker_thread = QtCore.QThread()
            new_worker.setObjectName(worker['WorkerObjectName'])
            new_worker_thread.setObjectName(worker['WorkerThreadName'])
            new_worker.moveToThread(new_worker_thread)

            # connect the worker signals to the MainWindow slots
            new_worker.worker_is_running.connect(self.disable_inputs)

            # this star an event loop on the thread, not the Worker.
            new_worker_thread.start()

            # add references of the worker and of the thread to the MainWindow
            # to avoid garbage collection
            self.workers[key] = new_worker
            self.worker_threads[worker['WorkerThreadName']] = new_worker_thread

    def connectSignalsSlot(self):
        """Connect Qt Signals to corresponding slots."""
        self.actionClose.triggered.connect(self.close)
        self.watchdog_pushbutton.clicked.connect(
            self.workers['FSWatchdog'].toggle)
        self.watchdog_pushbutton.clicked.connect(
            self.workers['FSMirror'].toggle)
        self.actionSta_rt_watchdog.triggered.connect(
            self.workers['FSWatchdog'].toggle)
        self.actionSta_rt_watchdog.triggered.connect(
            self.workers['FSMirror'].toggle)
        self.actionSta_rt_watchdog.triggered.connect(self.toggled_watchdog)
        self.actionStop_watchdog.triggered.connect(
            self.workers['FSWatchdog'].toggle)
        self.actionStop_watchdog.triggered.connect(
            self.workers['FSMirror'].toggle)
        self.actionStop_watchdog.triggered.connect(self.toggled_watchdog)
        self.action_Load_experiment.triggered.connect(self.load_experiment)
        self.actionSave_experiment.triggered.connect(self.save_experiment)
        self.actionSave_logger.triggered.connect(self.save_logger)
        self.actionClear_logger.triggered.connect(self.clear_logger)
        self.actionSet_engine.triggered.connect(
            self.open_mirroring_engine_selector)
        self.actionLoad_configuration_file.triggered.connect(
            self.load_conffile)
        self.actionAbout_Autologbook.triggered.connect(self.show_about)
        self.actionReset_to_default.triggered.connect(self.reset_conf)
        self.actionEdit_configuration.triggered.connect(self.edit_conf)
        self.actionChange_user_credentials.triggered.connect(
            self.edit_user_credentials)
        self.app.aboutToQuit.connect(self.force_quit)

    def edit_conf(self):
        """
        Open the configuration editor window.

        After closing the window the following actions are processed:
            1. The configuration information from the window are transferred to
               the local dictionary
            2. The autotools.init function is called in order to initialize all
               sub-modules global variables.
            3. Inputs of the main window are validated.

        Returns
        -------
        None.

        """
        dialog = ConfigurationEditorDialog(self)
        dialog.setAllValues(self.config)
        if dialog.exec_():
            self.config = dialog.get_conf()
            autotools.init(self.config)
            log.info('Configuration updated')
            self.are_user_credentials_checked = False
            self.validate_inputs()

    def load_conffile(self):
        """
        Load a configuration file.

        This function is called from the GUI and allows the user to load presets
        from a configuration file.

        It opens a file selection dialog restricted to *.ini file.
        If the user click on open, the following actions are processed:
            1. A configuration parser is created and the configuration file is parsed
            2. The autotools.init function is called
            3. The configuration object is assigned to the local configuration
            4. The inputs of the main window are validated.

        Returns
        -------
        None.

        """
        directory = Path.home() / Path('Documents')
        returnpath = QFileDialog.getOpenFileName(
            self, 'Configuration file', directory=str(directory), filter='Conf file (*.ini)')
        if returnpath:
            conffile = Path(returnpath[0])
            conf = configparser.ConfigParser()
            conf.read(conffile)
            autotools.init(conf)
            self.config = conf
            log.info('Loading configuration file %s' % (str(conffile)))
            self.are_user_credentials_checked = False
            self.validate_inputs()

    def reset_conf(self):
        """
        Reset the configuration to the default.

        A new configuration object is created using the autotools.generate_default_conf()
        The autotools.init function is called.
        The local configuration object is reassigned.

        Returns
        -------
        None.

        """
        conf = autotools.generate_default_conf()
        autotools.init(conf)
        self.config = conf
        log.info('Loading default configuration')
        self.are_user_credentials_checked = False
        self.validate_inputs()

    def force_quit(self):
        """
        Force quit the application.

        This function is called by the about to quit signal. It allows to
        quit as clean as possible all the open and running threads.

        Returns
        -------
        None.

        """
        for worker in self.workers.values():
            try:
                if worker.observer.is_alive():
                    worker.stop()
            except AttributeError:
                log.debug('Trying to quit an observer that was not created yet.')
        for thread in self.worker_threads.values():
            if thread.isRunning():
                thread.quit()
                thread.wait()

        if self.is_watchdog_running and self.is_mirroring_requested:
            # we need to kill the mirroring thread
            self.stopMirroring()

    @Slot(str, logging.LogRecord)
    def update_status(self, status, record):
        """
        Update the status window.

        This is the Qt Slot connected to the QtHandler Signaller.

        Parameters
        ----------
        status : STRING
            The formatted string to be appended to the message window.
        record : logging.LogRecord
            The LogRecord as transmitted by the logging module.

        Returns
        -------
        None.

        """
        color = self.COLORS.get(record.levelno, 'black')
        s = '<pre><font color="%s">%s</font></pre>' % (color, status)
        self.log_message_box.appendHtml(s)

    def watchdog_pushbutton_facelift(self):
        """
        Adapt the main window appearence.

        Depending on the fact that the wathdog is running or not, the main window
        has to look differently. This function is performing a facelift of the main window

        Returns
        -------
        None.

        """
        if self.is_watchdog_running:
            self.watchdog_pushbutton.setText('Stop watchdog')
            icon3 = QtGui.QIcon()
            icon3.addPixmap(QtGui.QPixmap(
                ":/resources/icons8-stop-sign-30.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.watchdog_pushbutton.setIcon(icon3)
            self.actionSta_rt_watchdog.setEnabled(False)
            self.actionEdit_configuration.setEnabled(False)
            self.actionStop_watchdog.setEnabled(True)
            self.open_explorer_pushbuttom.setEnabled(True)
            self.edit_custom_html_file_pushbutton.setEnabled(True)
            self.action_Load_experiment.setEnabled(False)
        else:
            self.watchdog_pushbutton.setText('Start watchdog')
            icon3 = QtGui.QIcon()
            icon3.addPixmap(QtGui.QPixmap(
                ":/resources/icons8-start-30.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.watchdog_pushbutton.setIcon(icon3)
            self.actionSta_rt_watchdog.setEnabled(True)
            self.actionEdit_configuration.setEnabled(True)
            self.actionStop_watchdog.setEnabled(False)
            self.open_explorer_pushbuttom.setEnabled(False)
            self.edit_custom_html_file_pushbutton.setEnabled(False)
            self.action_Load_experiment.setEnabled(True)

    def setMirroringEngine(self, engine):
        """
        Set the mirroring engine.

        Parameters
        ----------
        engine : string
            The name of the mirroring enging. Accepted options are:
                1. watchdog
                2. robocopy
            If an invalid name is provided, then the mirroring engine is set to
            watchdog and a warning message is displayed.

        Returns
        -------
        None.

        """
        if engine in ('watchdog', 'robocopy'):
            self.mirroringEngine = engine
        else:
            self.mirroringEngine = 'watchdog'
            log.warning(
                'Provided mirroring engine not recognized. Using default (watchdog)')

        # validate the inputs. If they were ok, they should be still ok, but
        # the process parameters are then resent to the workers
        self.validate_inputs()

    def changed_microscope(self, microscope):
        """
        Change the microscope.

        Parameters
        ----------
        microscope : name of the microscope
            For the moment the following microscopes are accepted:
                1. Quattro.
                2. Versa.
            If an invalid name is provided, the microscope is set back to Quattro

        Returns
        -------
        None.

        """
        log.info('Setting protocol parameters for microscope %s', microscope)
        self.microscope = microscope
        if microscope not in ['Quattro', 'Versa']:
            self.microscope = 'Quattro'
            log.error(
                'Microscope %s not yet implemented, reverting to default Quattro', microscope)
            self.select_microscope_comboBox.setCurrentText('Quattro')

    @Slot(bool)
    def disable_inputs(self, setDisable=True):
        """
        Disable the main window inputs.

        As soon as the watchdog is started, it is important to disable the
        input fields to avoid possible problems.

        Parameters
        ----------
        setDisable : bool, optional
            If set to False, the inputs will be enabled. The default is True.

        Returns
        -------
        None.

        """
        self.protocol_folder_text.setEnabled(not setDisable)
        self.select_protocol_folder.setEnabled(not setDisable)
        if self.is_mirroring_requested:
            self.mirroring_folder_text.setEnabled(not setDisable)
        if self.is_custom_ownership_requested:
            self.projectID_field.setEnabled(not setDisable)
            self.project_name_field.setEnabled(not setDisable)
            self.responsible_field.setEnabled(not setDisable)
        self.select_mirroring_folder.setEnabled(not setDisable)
        self.mirror_checkBox.setEnabled(not setDisable)
        self.select_microscope_comboBox.setEnabled(not setDisable)
        self.custom_ownership_checkbox.setEnabled(not setDisable)

    @Slot(bool)
    def toggled_mirroring(self, toggled):
        """
        Act upon a change in the mirror_checkBok.

        Parameters
        ----------
        toggled : bool
            the status.

        Returns
        -------
        None.

        """
        if self.mirror_checkBox.isChecked():
            self.is_mirroring_requested = True
        else:
            self.is_mirroring_requested = False
        self.validate_inputs()

    @Slot(bool)
    def toggled_custom_ownership(self, toggled):
        """
        Act upon a change in the custom_ownership_checkbox.

        Parameters
        ----------
        toggled : bool
            the status.

        Returns
        -------
        None.
        """
        if self.custom_ownership_checkbox.isChecked():
            self.is_custom_ownership_requested = True
        else:
            self.is_custom_ownership_requested = False
        self.validate_inputs()

    @Slot()
    def toggled_watchdog(self):
        """
        Emulate the behavior of a toggle button.

        The watchdog pushbutton has to work like a toggle switch.
        You press it once and the process starts, you press it again and
        it stops.

        We can perform also a facelift to the push button to change its
        text and the icon.

        Returns
        -------
        None.

        """
        # first change the status of the watchdog
        self.is_watchdog_running = not self.is_watchdog_running

        # update the pushbutton appearence
        self.watchdog_pushbutton_facelift()

    def open_browser(self):
        """
        Open a resource browser pointin to the monitored folder.

        Returns
        -------
        None.

        """
        command = 'explorer {}'.format(self.path)
        self.browser_process = subprocess.Popen(command.split())

    def open_yaml_editor(self):
        """
        Open the protocol editor.

        Returns
        -------
        None.

        """
        if not self.protocol_editor:
            self.protocol_editor = ProtocolEditor(
                parent=self, autolog=self.workers['FSWatchdog'].autolog)
        self.protocol_editor.show()
        self.protocol_editor.raise_()
        self.protocol_editor.activateWindow()

    @Slot()
    def open_protocol_folder(self):
        """Open a file dialog for the protocol folder."""
        directory = self.protocol_folder_text.text()
        if not directory:
            directory = str(Path(autoconfig.IMAGE_SERVER_BASE_PATH))
        returnpath = QFileDialog.getExistingDirectory(
            self, 'Select a protocol folder', directory=directory)
        if returnpath:
            returnpath = Path(returnpath)
            self.protocol_folder_path = returnpath
            self.protocol_folder_text.setText(str(returnpath))
            self.validate_inputs()

    @Slot()
    def open_mirroring_folder(self):
        """Open a file dialog for the mirroring folder."""
        directory = self.protocol_folder_text.text()
        if not directory:
            directory = str(Path(autoconfig.IMAGE_SERVER_BASE_PATH))
        returnpath = QFileDialog.getExistingDirectory(self, 'Select a mirroring folder',
                                                      directory=directory)
        if returnpath:
            returnpath = Path(returnpath)
            self.mirroring_folder_path = returnpath
            self.mirroring_folder_text.setText(str(returnpath))
            self.validate_inputs()

    @Slot()
    def protocol_folder_text_changed(self):
        """
        React to a change in the protocol folder field.

        This slot is connected to the protocol_folder_text editingFinished signal
        Convert the new text in a Path object and assign it to the protocol_folder_path
        variable.
        Call the validate_inputs method to verify if all inputs are ok and eventually
        enable the watchdog.

        Returns
        -------
        None.

        """
        pass
        # print('chi mi ha chiamato!')
        # if self.protocol_folder_text.text():
        #     self.protocol_folder_path = Path(self.protocol_folder_text.text())
        # self.validate_inputs()

    @Slot()
    def mirroring_folder_text_changed(self):
        """
        React to a change in the mirroring folder field.

        This slot is connected to the mirroring_folder_text editingFinished signal
        Convert the new text in a Path object and assign it to the mirroring_folder_path
        variable.
        Call the validate_inputs method to verify if all inputs are ok and eventually
        enable the watchdog.

        Returns
        -------
        None.

        """
        pass
        # if self.mirroring_folder_text.text():
        #     self.mirroring_folder_path = Path(
        #         self.mirroring_folder_text.text())
        # self.validate_inputs()

    def validate_inputs(self):  # noqa: C901
        """
        Validate all inputs.

        The input_folder can be local on the microscope PC or directly on the
        image server, while the mirroring_folder must be on the image server.

        We need to check that:
            1. The protocol folder is not Invalid. If Invalid just quit.
            2. If the mirroring switch is selected then:
                2.1 Check that the Mirroring folder is not Invalid
                2.2 If the custom ownership is requested:
                    2.2.1 Are the custom ownership fields ok?
                        2.2.1.1 If yes: The mirroring can be Acceptable or
                                AcceptableIfCustomOwnership
                        2.2.1.2 If No: The mirroring must be Acceptable
                2.3 If the custom ownership is not requested:
                    2.3.1 The mirroring must be Acceptable
            3. If the mirroring switch is not selected then:
                3.1 If the custom ownership is requested:
                    3.1.1 Are the custom ownership fields ok?
                        3.1.1.1 If yes: the protocol folder can be Acceptable or
                                AcceptableIfCustomOwnership
                        3.1.1.2 If no: the protocol folder must be Acceptable.
                3.2 If the custom ownership is not requested:
                    3.2.1 The protocol folder must be Acceptable

        Returns
        -------
        None.

        """
        protocol_folder = PathValidator(self.protocol_folder_text.text(
        ), autoconfig.IMAGE_SERVER_BASE_PATH, self.pattern)
        protocol_folder_validity = protocol_folder.validate()
        protocol_ownership_variables = protocol_folder.getOwnershipParameters()

        mirroring_folder = PathValidator(self.mirroring_folder_text.text(
        ), autoconfig.IMAGE_SERVER_BASE_PATH, self.pattern)
        mirroring_folder_validity = mirroring_folder.validate()
        mirroring_ownership_variables = mirroring_folder.getOwnershipParameters()

        custom_ownership_validity = self.projectID_field.text() and \
            self.project_name_field.text() and \
            self.responsible_field.text()

        # Condition 1
        if protocol_folder_validity != PathValidator.Invalid:
            # transfer the field text to the variable
            self.protocol_folder_path = Path(self.protocol_folder_text.text())
        else:
            # check if the field text is not empty
            if self.protocol_folder_text.text():
                # print a warning message
                log.warning('Protocol input folder is invalid')
            self.enable_watchdog(False)
            # stop here, it doesn't make sense to continue
            return

        # Condition 2
        if self.is_mirroring_requested:
            # if we get here the protocol_folder_validity is for sure not Invalid

            # Condition 2.1
            if mirroring_folder_validity != PathValidator.Invalid:
                # the mirroring folder is either Acceptable, AccetableIfMirroring or
                # AcceptableIfCustomOwnership

                # Condition 2.2
                if self.is_custom_ownership_requested:

                    # Condition 2.2.1
                    if custom_ownership_validity:
                        self.projectID = self.projectID_field.text()
                        self.project_name = self.project_name_field.text()
                        self.project_responsible = self.responsible_field.text()

                        # Condition 2.2.1.1
                        if mirroring_folder_validity in (PathValidator.Acceptable,
                                                         PathValidator.AcceptableIfCustomOwnership):
                            # we are good to go
                            # transfer the field texts to the parameters and enable the
                            # watchdog
                            self.mirroring_folder_path = Path(
                                self.mirroring_folder_text.text())
                            self.enable_watchdog(
                                True and self.are_user_credentials_ok())

                            if mirroring_folder_validity == PathValidator.Acceptable:
                                # inform the user that the custom ownership variables
                                # will be used
                                log.info('Custom parameters will be used (#=%s, Project=%s, Responsible=%s)' %
                                         (self.projectID, self.project_name, self.project_responsible))

                            return
                        else:
                            if mirroring_folder_validity == PathValidator.AcceptableIfCustomOwnership:
                                log.warning(
                                    'Please specify all three custom paramters')
                            self.enable_watchdog(False)

                    else:
                        # the three ownership fields are empty
                        self.projectID = None
                        self.project_name = None
                        self.project_responsible = None

                        # Condition 2.2.1.2
                        if mirroring_folder_validity == PathValidator.Acceptable:

                            # we are good to go
                            # transfer the field texts to the parameters and enable the
                            # watchdog
                            self.mirroring_folder_path = Path(
                                self.mirroring_folder_text.text())
                            self.enable_watchdog(
                                True and self.are_user_credentials_ok())
                            self.projectID_field.setText(
                                mirroring_ownership_variables[0])
                            self.project_name_field.setText(
                                mirroring_ownership_variables[1])
                            self.responsible_field.setText(
                                mirroring_ownership_variables[2])

                            return

                        else:
                            log.warning(
                                'Please specify all three custom paramters')
                            self.enable_watchdog(False)
                            # stop here, it doesn't make sense to continue
                            return

                # Condition 2.3
                else:
                    self.projectID = None
                    self.project_name = None
                    self.project_responsible = None

                    # Condition 2.3.1
                    if mirroring_folder_validity == PathValidator.Acceptable:
                        # we are good to go
                        # transfer the field texts to the parameters and enable the
                        # watchdog
                        self.mirroring_folder_path = Path(
                            self.mirroring_folder_text.text())
                        self.enable_watchdog(
                            True and self.are_user_credentials_ok())

                        self.enable_watchdog(
                            True and self.are_user_credentials_ok())
                        self.projectID_field.setText(
                            mirroring_ownership_variables[0])
                        self.project_name_field.setText(
                            mirroring_ownership_variables[1])
                        self.responsible_field.setText(
                            mirroring_ownership_variables[2])

                        return

                    else:
                        if mirroring_folder_validity == PathValidator.AcceptableIfCustomOwnership:
                            log.warning(
                                'Please activate Use custom parameters')
                            log.warning(
                                'Please specify all three custom paramters')
                        else:
                            if self.mirroring_folder_text.text():
                                # print the error message only if the input field is
                                # not empty
                                log.error('Mirroring folder is invalid')
                        self.enable_watchdog(False)

            else:
                # the mirroring folder is Invalid.
                # check if the field text is not empty
                if self.mirroring_folder_text.text():
                    # print the error message only if the input field is
                    # not empty
                    log.error('Mirroring folder is invalid')
                self.enable_watchdog(False)

        # Condition 3
        # the mirroring is not requested.
        else:

            # Condition 3.1
            if self.is_custom_ownership_requested:

                # Condition 3.1.1
                if custom_ownership_validity:
                    self.projectID = self.projectID_field.text()
                    self.project_name = self.project_name_field.text()
                    self.project_responsible = self.responsible_field.text()

                    # Condition 3.1.1.1
                    if protocol_folder_validity in (PathValidator.Acceptable,
                                                    PathValidator.AcceptableIfCustomOwnership):
                        # we are good to go
                        # transfer the field texts to the parameters and enable the
                        # watchdog
                        self.protocol_folder_path = Path(
                            self.protocol_folder_text.text())
                        self.enable_watchdog(
                            True and self.are_user_credentials_ok())
                        return
                    else:
                        # all other cases should be already analyzed
                        log.warning(
                            'The protocol folder is valid only if mirroring is selected')
                        self.enable_watchdog(False)
                else:
                    # the three ownership fields are empty
                    self.projectID = None
                    self.project_name = None
                    self.project_responsible = None

                    # Condition 3.1.1.2
                    if protocol_folder_validity == PathValidator.Acceptable:
                        # we are good to go
                        # transfer the field texts to the parameters and enable the
                        # watchdog
                        self.protocol_folder_path = Path(
                            self.protocol_folder_text.text())
                        self.enable_watchdog(
                            True and self.are_user_credentials_ok())

                        # display the ownership variables in the disable field
                        self.enable_watchdog(
                            True and self.are_user_credentials_ok())
                        self.projectID_field.setText(
                            protocol_ownership_variables[0])
                        self.project_name_field.setText(
                            protocol_ownership_variables[1])
                        self.responsible_field.setText(
                            protocol_ownership_variables[2])

                        return
                    else:
                        # all other cases should be already analyzed
                        log.warning(
                            'The protocol folder is valid only if mirroring is selected')
                        if protocol_ownership_variables:
                            self.projectID_field.setText(
                                protocol_ownership_variables[0])
                            self.project_name_field.setText(
                                protocol_ownership_variables[1])
                            self.responsible_field.setText(
                                protocol_ownership_variables[2])
                        self.enable_watchdog(False)

            # Condition 3.2
            else:

                self.projectID = None
                self.project_name = None
                self.project_responsible = None

                # Condition 3.2.1
                if protocol_folder_validity == PathValidator.Acceptable:
                    # we are good to go
                    # transfer the field texts to the parameters and enable the
                    # watchdog
                    self.protocol_folder_path = Path(
                        self.protocol_folder_text.text())
                    self.enable_watchdog(
                        True and self.are_user_credentials_ok())
                    # fill in the ownership field with the guessed values
                    self.projectID_field.setText(
                        protocol_ownership_variables[0])
                    self.project_name_field.setText(
                        protocol_ownership_variables[1])
                    self.responsible_field.setText(
                        protocol_ownership_variables[2])

                    return
                else:
                    # all other cases should be already analyzed
                    log.warning(
                        'The protocol folder is valid only if mirroring is selected')
                    if protocol_ownership_variables:
                        self.projectID_field.setText(
                            protocol_ownership_variables[0])
                        self.project_name_field.setText(
                            protocol_ownership_variables[1])
                        self.responsible_field.setText(
                            protocol_ownership_variables[2])
                    self.enable_watchdog(False)

    def are_user_credentials_ok(self):
        """
        Check whether the user credentials are ok.

        If the credentianls were never checked before, perform a validity check
        trying to connect to the elog and download some numbers.

        If the check fails, the user is prompted with a dialog window to re-introduce
        the credentials. This occurs in a loop with a maximum number of repetition
        defined by the configuration variable max_auth_error.

        Returns
        -------
        bool
            The status of the user credentials..

        """
        if not self.are_user_credentials_checked:
            for i in range(self.config.getint('elog', 'max_auth_error')):
                if self._are_user_credentials_ok():
                    return True
                    break
                else:
                    self._edit_user_credentials()
            log.error('Wrong user name and password.')
            log.error(
                'Use Settings/Change User credetials to correct the problem and continue.')
            return False
        else:
            self.are_user_credentials_checked = True
            return True

    def _are_user_credentials_ok(self):
        try:
            elog_instance = elog.open(
                hostname=self.config['elog']['elog_hostname'],
                port=self.config['elog']['elog_port'],
                user=self.config['elog']['elog_user'],
                password=self.config['elog']['elog_password'],
                use_ssl=True,
                encrypt_pwd=False,
                logbook=self.config[self.select_microscope_comboBox.currentText(
                )]['logbook']
            )

            elog_instance.get_message_ids()
        except elog.LogbookAuthenticationError:
            return False
        return True

    def edit_user_credentials(self):
        """Open the user credentials dialog."""
        self._edit_user_credentials()
        self.validate_inputs()

    def _edit_user_credentials(self):
        dialog = UserEditor(self, username=self.config['elog']['elog_user'],
                            password=self.config['elog']['elog_password'])
        if dialog.exec_():
            self.config['elog']['elog_user'] = dialog.username
            self.config['elog']['elog_password'] = dialog.password
            autotools.init(self.config)
            self.are_user_credentials_checked = False

    def enable_watchdog(self, is_ok):
        """
        Make the watchdog able to start.

        this methos is called after the input validation.

        Parameters
        ----------
        is_ok : BOOL
            If True, the watchdog is enabled and the relevant parameters are
            transferred to the Worker

        Returns
        -------
        None.

        """
        self.watchdog_pushbutton.setEnabled(is_ok)
        self.actionSta_rt_watchdog.setEnabled(is_ok)
        self.is_watchdog_enabled = is_ok
        self.actionSave_experiment.setEnabled(is_ok)
        if is_ok:
            self.path = self.protocol_folder_path
            if self.mirror_checkBox.isChecked():
                self.path = self.mirroring_folder_path
            self.workers['FSWatchdog'].updateParameters(path=self.path,
                                                        microscope=self.select_microscope_comboBox.currentText(),
                                                        projectID=self.projectID,
                                                        project_name=self.project_name,
                                                        responsible=self.project_responsible)

            self.change_autolog.emit(self.workers['FSWatchdog'].autolog)

            if not self.is_mirroring_requested:
                # just send useless data
                self.mirroring_folder_path = self.protocol_folder_path
            self.workers['FSMirror'].updateParameters(src_path=self.protocol_folder_path,
                                                      dst_path=self.mirroring_folder_path,
                                                      is_required=self.is_mirroring_requested,
                                                      engine=self.mirroringEngine)
            log.info('Folder selection is ok. Ready to start the watchdog')

    @Slot()
    def clear_logger(self):
        """
        Clear the logger message box.

        This slot is called by the clear logger button clicked event

        Returns
        -------
        None.

        """
        self.log_message_box.clear()

    @Slot()
    def save_logger(self):
        """
        Save the content of the logger message box.

        The user has the possibility to save the content as a simple plain text
        or as a formatted HTML document, since the document is actually originally
        formatted as HTML.

        Returns
        -------
        None.

        """
        directory = Path.home() / Path('Documents')
        logger_file = QFileDialog.getSaveFileName(self, 'Logger file name',
                                                  filter='HTML file (*.html);;Text file (*.txt)',
                                                  directory=str(directory))
        if logger_file[0]:
            if logger_file[1] == 'HTML file (*.html)':
                text = str(self.log_message_box.document().toHtml())
            elif logger_file[1] == 'Text file (*.txt)':
                text = str(self.log_message_box.toPlainText())
            else:
                text = 'Wrong format'
            with open(Path(logger_file[0]), 'w') as lf:
                lf.write(text)

    def open_mirroring_engine_selector(self):
        """
        Allow the selection of a mirroring engine.

        Instead of opening the configuration editor, the user has the possibility
        to just select the mirroring engine from this small dialog.

        The dialog is executed in Dialog Modal mode.

        Returns
        -------
        None.

        """
        dialog = MirroringEngineDiaolog(self)
        if dialog.exec_():
            self.setMirroringEngine(dialog.comboBox.currentText())
            log.info('Mirroring engine set to %s' %
                     dialog.comboBox.currentText())

    def show_about(self):
        """
        Show the about dialog.

        Returns
        -------
        None.

        """
        dialog = AboutDialog(self)
        dialog.setWindowFlags(QtCore.Qt.WindowTitleHint
                              | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowTitleHint)
        dialog.exec_()

    def load_experiment(self):
        """
        Load an experiment file.

        An experiment file is a modified version of a configuration file with a
        dedicated section to the GUI. In this way, all GUI fields are preset
        to the values stored in the file.

        After loading, the validate_inputs method is called so that if everything
        is ok, the Start Watchdog is enabled and all parameters are sent to the
        workers.

        Returns
        -------
        None.

        """
        directory = Path.home() / 'Documents'
        returnpath = QFileDialog.getOpenFileName(self, 'Open experiment file',
                                                 directory=str(directory),
                                                 filter='Experiments (*.exp)')
        if returnpath[0]:
            self._load_experiment(returnpath[0])

    def _load_experiment(self, path):
        config = autotools.safe_configread(path)
        self.config = config
        autotools.init(config)
        self.protocol_folder_text.setText(
            str(Path(config['GUI']['src_path'])))
        if config['GUI']['mirror_path']:
            self.mirroring_folder_text.setText(
                str(Path(config['GUI']['mirror_path'])))
        else:
            self.mirroring_folder_text.clear()
        self.mirror_checkBox.setChecked(config.getboolean('GUI', 'mirror'))
        self.select_microscope_comboBox.setCurrentText(
            config['GUI']['microscope'])
        self.custom_ownership_checkbox.setChecked(
            config.getboolean('GUI', 'custom_ownership', fallback=False))
        self.projectID_field.setText(
            config.get('GUI', 'projectID', fallback=''))
        self.project_name_field.setText(
            config.get('GUI', 'project_name', fallback=''))
        self.responsible_field.setText(
            config.get('GUI', 'responsible', fallback=''))

        self.watchdog_pushbutton.setFocus()
        log.info('Loaded experiment %s and updated configuration' %
                 str(Path(path)))
        self.are_user_credentials_checked = False
        self.validate_inputs()

    def save_experiment(self):
        """
        Save the experiment file.

        An experiment file is a modified version of a configuration file with a
        dedicated section to the GUI. In this way, all GUI fields are preset
        to the values stored in the file.

        Returns
        -------
        None.

        """
        directory = Path.home() / 'Documents'
        returnpath = QFileDialog.getSaveFileName(self, 'Save experiment file',
                                                 directory=str(directory), filter='Experiments (*.exp)')
        if returnpath[0]:
            if not self.mirroring_folder_text.text():
                mirror_path = ''
            else:
                mirror_path = str(Path(self.mirroring_folder_text.text()))

            if self.custom_ownership_checkbox.isChecked():
                projectID = self.projectID_field.text()
                project_name = self.project_name_field.text()
                responsible = self.responsible_field.text()
            else:
                projectID = ''
                project_name = ''
                responsible = ''

            self.config['GUI'] = {
                'src_path': str(Path(self.protocol_folder_text.text())),
                'mirror_path': mirror_path,
                'mirror': self.mirror_checkBox.isChecked(),
                'microscope': self.select_microscope_comboBox.currentText(),
                'custom_ownership': self.custom_ownership_checkbox.isChecked(),
                'projectID': projectID,
                'project_name': project_name,
                'responsible': responsible,
            }
            with open(returnpath[0], 'w') as f:
                self.config.write(f)
            log.info('Experiment file save to %s' % str(Path(returnpath[0])))


def override_credentials(args, config):
    """
    Override configuration file provided user credentials.

    If the user provides username and/or password from the command line,
    these have the priority over credentials stored in configuration files.

    **NOTE**
    Credentials saved in experiment files are **NOT** overriden!

    Parameters
    ----------
    args : dictionary
        The dictionary of command line arguments as obtained from the
        parse_arguments.
    config : dictionary
        The configuration dictionary as provided by the configuration parser.

    Returns
    -------
    None.

    """
    if args.username:
        config['elog']['elog_user'] = args.username
        # if username is provided, check if password is provided as well.
        # if no password is provided, set it to None so that the dialog window
        # will show up
        if args.password:
            config['elog']['elog_password'] = autotools.encrypt_pass(
                args.password)
        else:
            config['elog']['elog_password'] = ''
    else:
        # this is strange but possible: the user just wants to override the password,
        # but not the username.
        if args.password:
            config['elog']['elog_password'] = autotools.encrypt_pass(
                args.password)


def main_gui(args):
    """
    Open the main window and start the Qt Event loop.

    Parameters
    ----------
    args : system arguments
        The system arguments can be provided when starting the app.

    Returns
    -------
    None.

    """
    # give a name at the main thread
    threading.current_thread().name = 'GUIThread'

    # prepare the logging machinery
    loglevel = autoconfig.LEVELS.get(args.loglevel.lower())
    log.setLevel(level=loglevel)

    # prepare the machinery for the configuration file parser
    config = configparser.ConfigParser()
    # check if the specified configuration file exists and loaded
    if not args.conffile.exists():
        # it looks like that the specified configuration file doesn't exist,
        # so we need to create one
        autotools.write_default_conffile(args.conffile)
    config = autotools.safe_configread(args.conffile)

    # if user provided username and password from the command line,
    # they must override the configuration file ones.
    override_credentials(args, config)

    # configure the whole package
    autotools.init(config)

    # start the Qt App
    app = QApplication(sys.argv)
    win = MainWindow(app, config)
    win.setMirroringEngine(args.engine)

    # if the user preloaded an experiment file, then do it here
    if args.expfile:
        try:
            win._load_experiment(args.expfile)
            # if the user wants to start the watchdog right away,
            # do it, but before check that it is ok to do it.
            if win.is_watchdog_enabled and args.autoexec:
                win.watchdog_pushbutton.clicked.emit()
        except elog.LogbookServerProblem as err:
            log.critical('Logbook server problem')
            log.exception(err)
        except elog.LogbookAuthenticationError:
            log.error('Wrong user name and password.')
            log.error(
                'Use Settings/Change User credetials to correct the problem and continue.')

    # show the main window
    win.show()

    # execute the main window and eventually exit when done!
    sys.exit(app.exec())
