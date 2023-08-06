#! python
import base64
import glob
import os
import shutil
import tkinter as ttk
from datetime import datetime
from io import BytesIO
from pathlib import Path
from tkinter import *
from tkinter import filedialog, scrolledtext
from tkinter.constants import END

import elog
import passlib
import tifffile
import urllib3
import win32com.client as win32
from PIL import Image, ImageGrab
from yattag import Doc

urllib3.disable_warnings()

elog_hostname = 'https://10.166.16.24/'
elog_port = 8080
elog_use_ssl = True
elog_user = 'log-robot'
elog_password = 'IchBinRoboter'
elog_encoding = 'HTML'

#
# function to convert an image in a base64 encoded string


def image_to_b64(image_path, maxwidth):
    with Image.open(image_path, "r") as image:
        w, h = image.size
        image.thumbnail((round(maxwidth), round(maxwidth * h / w)))
        buff = BytesIO()
        image.save(buff, format="JPEG")
        img_str = base64.b64encode(buff.getvalue())
        return img_str.decode('utf-8')

#
# Convert BMPs to PNGs
#


class ConvertBMPtoPNG(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("BMP converter")
        mainframe = ttk.Frame(self)
        mainframe.grid(padx=20, pady=20)
        ttk.Label(mainframe, text="Convert BMP images in PNG format", font=(
            "Arial", 24)).grid(column=0, row=0, padx=20, pady=20, columnspan=3, sticky="EW")
        ttk.Label(mainframe, text="Use this tool to convert all BMP files present in a directory and in all its subdirectories in PNG. Click the Select a folder button to select the parent folder, the conversion will start automatically.").grid(
            column=0, row=1, padx=5, pady=5, columnspan=3, sticky="EW")
        # ttk.Label(mainframe, text ="List of selected files").grid(column=0, row=2, padx=0, pady=0, columnspan=1, sticky="EW")
        self.filelist_scrolltext = scrolledtext.ScrolledText(
            mainframe, width=40, height=10)
        self.filelist_scrolltext.grid(
            column=0, row=3, padx=20, pady=20, columnspan=3, sticky="EW")

        # select director button
        select_directory_button = ttk.Button(
            mainframe, text="Select a folder...", command=self.select_folder)
        select_directory_button.grid(
            column=0, row=4, padx=5, pady=5, sticky="ew")
        self.parent_folder = ""

        # close button
        ttk.Button(mainframe, text="Close", command=self.destroy).grid(
            column=2, row=4, columnspan=1, padx=5, pady=5, sticky="ew")

    def select_folder(self):
        self.parent_folder = filedialog.askdirectory(
            parent=self, title="Select a parent folder",)
        self.filelist_scrolltext.insert(
            END, "Starting from " + self.parent_folder + "\n")
        int_dirs = []
        bmpfiles = []
        for curdir, dirs, files in os.walk(self.parent_folder, topdown=True):
            for file in files:
                # print ("File: " +file)
                if os.path.splitext(file)[1] == '.bmp':
                    bmpfiles.append(os.path.join(curdir, file))
                    if curdir not in int_dirs:
                        int_dirs.append(curdir)
        for file in bmpfiles:
            self.filelist_scrolltext.insert(END, "Converting " + file)
            try:
                Image.open(file).save(os.path.splitext(file)[0] + '.png')
                self.filelist_scrolltext.insert(END, " done!\n")
            except:
                self.filelist_scrolltext.insert(END, " FAILED!\n")

        for dir in int_dirs:
            self.filelist_scrolltext.insert(
                END, "Making " + os.path.join(dir, "orig-bmp"))
            try:
                os.mkdir(os.path.join(dir, "orig-bmp"))
                self.filelist_scrolltext.insert(END, " done!\n")
            except OSError as error:
                self.filelist_scrolltext.insert(END, " FAILED!\n")

            # command = 'copy ' + os.path.join(dir, "*.bmp") + ' ' + os.path.join(dir, "orig-bmp")
            for file in glob.glob(os.path.join(dir, '*.bmp')):
                self.filelist_scrolltext.insert(
                    END, "Moving " + file + ' to ' + os.path.join(dir, "orig-bmp"))
                try:
                    shutil.move(file, os.path.join(dir, "orig-bmp"))
                    self.filelist_scrolltext.insert(END, " done!\n")
                except:
                    self.filelist_scrolltext.insert(END, " FAILED!\n")

            # os.system('copy ' + os.path.join(dir, "*.bmp") + ' ' + os.path.join(dir, "orig-bmp"))


#
# RemoveDatabarFromTIF
#
class RemoveDatabarFromTIF(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.parent_folder = ''
        self.title("Remove databar")
        mainframe = ttk.Frame(self)
        mainframe.grid(padx=20, pady=20)
        ttk.Label(mainframe, text="Remove databar from FEI TIFF", font=("Arial", 24)).grid(
            column=0, row=0, padx=20, pady=20, columnspan=3, sticky="EW")
        ttk.Label(mainframe, text="Use this tool to crop the databar from TIFF images. This tool assumes that the images were acquired using an ThermoFisher/FEI Microscope.\nAll TIFF images with a databar contained in the selected folder will be processed.").grid(
            column=0, row=1, padx=5, pady=5, columnspan=3, sticky="EW")
        self.filelist_scrolltext = scrolledtext.ScrolledText(
            mainframe, width=40, height=10)
        self.filelist_scrolltext.grid(
            column=0, row=3, padx=20, pady=20, columnspan=3, sticky="EW")

        # select director button
        select_directory_button = ttk.Button(
            mainframe, text="Select a folder...", command=self.select_folder)
        select_directory_button.grid(
            column=0, row=4, padx=5, pady=5, sticky="ew")

        # close button
        ttk.Button(mainframe, text="Close", command=self.destroy).grid(
            column=2, row=4, columnspan=1, padx=5, pady=5, sticky="ew")

    def select_folder(self):
        self.parent_folder = filedialog.askdirectory(
            parent=self, title="Select a parent folder")
        self.filelist_scrolltext.insert(
            END, "Converting TIFF images in " + self.parent_folder + "\n")
        for file in glob.glob(os.path.join(self.parent_folder, '*.tif*')):
            self.filelist_scrolltext.insert(END, "Processing... " + file)
            with tifffile.TiffFile(file) as tif:
                # first check if the tiff file comes from the FEI microscope
                if not tif.is_fei:
                    self.filelist_scrolltext.insert(
                        END, " FAILED! (not a FEI file)\n")
                else:
                    # check if there a data bar.
                    # if the image shape is different from the scan size, then there a databar
                    # and the image must be cropped_img
                    page = tif.pages[0]
                    image = page.asarray()
                    image_width = page.tags['ImageWidth'].value
                    image_height = page.tags['ImageLength'].value
                    scan_width = tif.fei_metadata['Image']['ResolutionX']
                    scan_height = tif.fei_metadata['Image']['ResolutionY']
                    if (image_width, image_height) != (scan_width, scan_height):
                        # ok, we need to crop!
                        crop_image = image[:scan_height, :scan_width]
                    else:
                        # the image is already without databar
                        # go ahead anyhow to perform TIF calibration
                        crop_image = image
                    pixel_width = tif.fei_metadata['Scan']['PixelWidth']
                    pixel_height = tif.fei_metadata['Scan']['PixelHeight']
                    xResolution = 1. / (pixel_width * 100)
                    yResolution = 1. / (pixel_height * 100)
                    sample = tif.fei_metadata['User']['UserText']
                    beam = tif.fei_metadata['Beam']['Beam']
                    HV = tif.fei_metadata['Beam']['HV']
                    if HV > 1000:
                        HV = HV / 1000
                        HV = str(HV) + 'kV'
                    else:
                        HV = str(HV) + 'V'
                    hfw = tif.fei_metadata[beam]['HFW']
                    dispwidth = tif.fei_metadata['System']['DisplayWidth']
                    magnification = round(dispwidth / hfw / 1.25)
                    if magnification > 1000:
                        magnification = round(magnification / 1000)
                        magnification = str(magnification) + 'kx'
                    else:
                        magnification = str(magnification) + 'x'
                    description = str(sample) + '-' + beam + \
                        '-' + HV + '-' + magnification

                    # finally ready to write the output file
                    output_filename = os.path.splitext(
                        file)[0] + '_no_databar' + os.path.splitext(file)[1]
                    with tifffile.TiffWriter(output_filename) as out:
                        out.write(
                            crop_image,
                            photometric=page.photometric,
                            compression=page.compression,
                            planarconfig=page.planarconfig,
                            rowsperstrip=page.rowsperstrip,
                            description=description,
                            software='labtools',
                            resolution=(
                                xResolution,
                                yResolution,
                                3  # cm
                            ),
                            extratags=[page.tags['FEI_HELIOS'].astuple(tif)]
                        )
                    self.filelist_scrolltext.insert(END, " done!\n")
        self.filelist_scrolltext.insert(END, "Finished!\n")

#
# Dialog for the protocol verification
#


class ProtocolVerification(Toplevel):
    def __init__(self, master=None, parent=None):

        super().__init__(master=master)
        self.parent = parent

        self.protocol_id_text = StringVar(self, self.parent.protocol)
        self.project_text = StringVar(self, value=self.parent.project)
        self.customer_text = StringVar(self, value=self.parent.customer)

        self.title("Quattro automatic Logbook")
        mainframe = ttk.Frame(self)
        mainframe.grid(padx=20, pady=20)
        ttk.Label(mainframe, text="Please verify and correct the protocol information", font=("Arial", 24)).grid(
            column=0, row=0, padx=20, pady=20, columnspan=3, sticky="EW")
        protocol_id_label = ttk.Label(mainframe, text='Protocol ID:')
        protocol_id_label.grid(column=0, row=1, padx=20, pady=20, sticky="EW")

        protocol_id_entry = ttk.Entry(
            mainframe, textvariable=self.protocol_id_text)
        protocol_id_entry.grid(column=1, row=1, padx=20, pady=20, sticky="EW")

        project_label = ttk.Label(mainframe, text='Project:')
        project_label.grid(column=0, row=2, padx=20, pady=20, sticky="EW")

        project_entry = ttk.Entry(mainframe, textvariable=self.project_text)
        project_entry.grid(column=1, row=2, padx=20, pady=20, sticky="EW")

        customer_label = ttk.Label(mainframe, text='Customer:')
        customer_label.grid(column=0, row=3, padx=20, pady=20, sticky="EW")

        customer_entry = ttk.Entry(mainframe, textvariable=self.customer_text)
        customer_entry.grid(column=1, row=3, padx=20, pady=20, sticky="EW")

        # close button
        ttk.Button(mainframe, text="Accept and close", command=self.dismiss).grid(
            column=2, row=4, columnspan=1, padx=5, pady=5, sticky="ew")

        # intercept close button
        self.protocol("WM_DELETE_WINDOW", self.dismiss)
        self.wait_visibility()
        self.grab_set()
        self.wait_window()

    def dismiss(self):
        self.protocol_id_text.get()
        self.project_text.get()
        self.customer_text.get()
        self.grab_release()
        self.destroy()


#
# QuattroLogbook
#
class QuattroLogbook(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Quattro automatic Logbook")
        mainframe = ttk.Frame(self)
        mainframe.grid(padx=20, pady=20)
        ttk.Label(mainframe, text="Automatic logbook generator", font=("Arial", 24)).grid(
            column=0, row=0, padx=20, pady=20, columnspan=3, sticky="EW")
        ttk.Label(mainframe, text="Use this tool generate logbook entries for Quattro Analysis.").grid(
            column=0, row=1, padx=5, pady=5, columnspan=3, sticky="EW")
        self.filelist_scrolltext = scrolledtext.ScrolledText(
            mainframe, width=40, height=10)
        self.filelist_scrolltext.grid(
            column=0, row=3, padx=20, pady=20, columnspan=3, sticky="EW")

        # select director button
        select_directory_button = ttk.Button(
            mainframe, text="Select a folder...", command=self.select_folder)
        select_directory_button.grid(
            column=0, row=4, padx=5, pady=5, sticky="ew")

        # close button
        ttk.Button(mainframe, text="Close", command=self.destroy).grid(
            column=2, row=4, columnspan=1, padx=5, pady=5, sticky="ew")

    def select_folder(self):

        self.parent_folder = filedialog.askdirectory(
            parent=self, title="Select an analysis folder")

        # check if the folder was named correctly.
        if len(Path(self.parent_folder).parts[-1].split('-')) != 3:
            self.protocol = Path(self.parent_folder).parts[-1]
            self.project = Path(self.parent_folder).parts[-1]
            self.customer = Path(self.parent_folder).parts[-1]
            dlg = ProtocolVerification(parent=self)
            self.protocol = dlg.protocol_id_text.get()
            self.project = dlg.project_text.get()
            self.customer = dlg.customer_text.get()
        else:
            self.protocol = Path(
                self.parent_folder).parts[-1].split('-')[0].strip()
            self.project = Path(
                self.parent_folder).parts[-1].split('-')[1].strip()
            self.customer = Path(
                self.parent_folder).parts[-1].split('-')[2].strip()

        self.elog_logbook = 'Quattro-Analysis'
        self.filelist_scrolltext.insert(
            END, "Generating logbook file for " + Path(self.parent_folder).parts[-1] + "\n")

        # the yattag for HTML code generation
        doc, tag, text = Doc().tagtext()

        # start preparing the message
        with tag('h1', style='text-align: center;'):
            text('Quatto SEM Analysis protocol {}'.format(self.protocol))
        with tag('h2'):
            text('Navigation image(s) of the sample stage')

        # the expected content of the parent folder is:
        # ** One or more Nav-Cam pictures
        # ** One or more pdf file, probably EDS/EBSD report
        # ** One or more subfolder for each sample with all the images

        # scan for nav-cam pics
        self.navcam_pics = glob.glob(
            os.path.join(self.parent_folder, '*Nav-Cam*'))
        self.filelist_scrolltext.insert(
            END, 'Found ' + str(len(self.navcam_pics)) + ' navigation picture(s)\n')

        # a bit of complication in order to arrange the nav pics inside a table
        if len(self.navcam_pics) == 1:
            with tag('table', align='left', border='1', cellpadding='1', cellspacing='1', style='width:500px; border-collapse:collapse'):
                with tag('tbody'):
                    with tag('tr'):
                        with tag('td'):
                            with tag('p', style='text-align-center'):
                                doc.stag('img', alt=self.navcam_pics[0], src='data:image/jpeg;base64, {}'.format(
                                    image_to_b64(self.navcam_pics[0], 490)))
        elif len(self.navcam_pics) > 1:
            with tag('table', align='left', border='1', cellpadding='1', cellspacing='1', style='width:1000px; border-collapse:collapse'):
                with tag('tbody'):
                    # calculate how many rows do we need
                    # n_full_row is the number of full rows
                    n_row = len(self.navcam_pics) / 2
                    n_full_row = int(n_row)
                    i = 0
                    for irow in range(0, n_full_row):
                        with tag('tr'):
                            with tag('td'):
                                with tag('p', style='text-align:center'):
                                    doc.stag('img', alt=self.navcam_pics[i], src='data:image/jpeg;base64, {}'.format(
                                        image_to_b64(self.navcam_pics[i], 490)))
                            i += 1
                            with tag('td'):
                                with tag('p', style='text-align:center'):
                                    doc.stag('img', alt=self.navcam_pics[i], src='data:image/jpeg;base64, {}'.format(
                                        image_to_b64(self.navcam_pics[i], 490)))

                    if n_row != n_full_row:
                        # we have to add an extra row with the last pic
                        with tag('tr'):
                            with tag('td', colspan=2):
                                with tag('p', style='text-align:center'):
                                    doc.stag('img', alt=self.navcam_pics[-1], src='data:image/jpeg;base64, {}'.format(
                                        image_to_b64(self.navcam_pics[-1], 490)))
        else:
            with tag('h2'):
                text('No navigation picture provided!')

        doc.asis('<br clear="all">')

        # scan for PDF reports
        self.pdf_reports = glob.glob(os.path.join(self.parent_folder, '*pdf'))
        self.filelist_scrolltext.insert(
            END, 'Found ' + str(len(self.pdf_reports)) + ' PDF reports(s)\n')

        # scan for folder (each folder a sample)
        self.sample_dirs = [f.path for f in os.scandir(
            self.parent_folder) if f.is_dir()]
        self.filelist_scrolltext.insert(
            END, 'Found ' + str(len(self.sample_dirs)) + ' sample(s)\n')

        if self.sample_dirs:
            # populating the sample description

            for sample in self.sample_dirs:
                sample_name = os.path.split(sample)[-1]
                images = glob.glob(os.path.join(sample, '*tif*'))
                if not images:
                    with tag('h2'):
                        doc.stag('hr')
                        text('No images found for {}\n'.format(sample_name))
                    self.filelist_scrolltext.insert(
                        END, 'Processing sample {} but no images found\n'.format(sample_name))
                else:
                    self.filelist_scrolltext.insert(
                        END, 'Processing sample ' + sample_name + ' with ' + str(len(images)) + ' pictures\n')
                    with tag('p'):
                        doc.stag('hr')
                    with tag('h2'):
                        text('Picture list for sample: {}'.format(sample_name))

                    hv = 0
                    beam = ''
                    magnification = 0
                    spotsize = 0

                    detector = ''

                    vacuum = ''
                    user_text = ''
                    id = 0

                    encoded_img = ''
                    maxwidth = 200

                    width = 0
                    height = 0
                    with tag('table', border=1, cellpaggind=1, cellspacing=1, style='width:1000px; border-collapse:collapse'):
                        with tag('tbody'):
                            for image in images:

                                # generate a png thumbnail for download
                                with Image.open(image) as inp:
                                    m = 640
                                    w, h = inp.size
                                    inp.thumbnail((round(m), round(m * h / w)))
                                    inp.convert('RGB')
                                    outputname = '{}'.format(
                                        os.path.splitext(image)[0] + '.png')
                                    inp.save(outputname)

                                # get the id from the file. this is the first part of the split
                                id = os.path.split(image)[-1].split('-')[0]

                                # open the tif image with tifffile to retrieve the fei_metadata
                                with tifffile.TiffFile(image) as tif:

                                    # first check if the tiff file comes from the FEI microscope
                                    if not tif.is_fei:
                                        self.filelist_scrolltext.insert(
                                            END, "Image " + image + " not FEI\n")
                                        hv = 'N/A'
                                        beam = 'N/A'
                                        magnification = 'N/A'
                                        spotsize = 'N/A'
                                        detector = 'N/A'
                                        vacuum = 'N/A'
                                        width = 'N/A'
                                        height = 'N/A'
                                    else:
                                        hv = tif.fei_metadata['Beam']['HV']
                                        if hv > 1000:
                                            hv = hv / 1000
                                            hv = str(hv) + 'kV'
                                        else:
                                            hv = str(hv) + 'V'

                                        beam = tif.fei_metadata['Beam']['Beam']

                                        hfw = tif.fei_metadata[beam]['HFW']
                                        dispwidth = tif.fei_metadata['System']['DisplayWidth']
                                        magnification = round(
                                            dispwidth / hfw / 1.25)
                                        if magnification > 1000:
                                            magnification = round(
                                                magnification / 1000)
                                            magnification = str(
                                                magnification) + 'kx'
                                        else:
                                            magnification = str(
                                                magnification) + 'x'

                                        spotsize = tif.fei_metadata['Beam']['Spot']

                                        detector = str(
                                            tif.fei_metadata['Detectors']['Mode']) + '.' + str(tif.fei_metadata['Detectors']['Name'])

                                        vacuum = str(
                                            tif.fei_metadata['Vacuum']['UserMode'])
                                        user_text = str(
                                            tif.fei_metadata['User']['UserText'])
                                        width = tif.fei_metadata['Image']['ResolutionX']
                                        height = tif.fei_metadata['Image']['ResolutionY']

                                    # generate the encoded_img
                                    encoded_img = image_to_b64(image, maxwidth)
                                    with tag('tr'):
                                        with tag('td', colspan=7, style='text-align:center;height:50px;background-color:cyan'):
                                            with tag('b'):
                                                text(image)
                                    with tag('tr'):
                                        with tag('th', colspan=2, rowspan=2):
                                            doc.stag('img', alt=os.path.split(image)[-1], src='data:image/jpeg;base64, {}'.format(
                                                encoded_img))
                                        with tag('td'):
                                            with tag('strong'):
                                                text('ID: ')
                                            text(id)
                                        with tag('td'):
                                            with tag('strong'):
                                                text('HV: ')
                                            text(hv)
                                        with tag('td'):
                                            with tag('strong'):
                                                text('Beam: ')
                                            text(beam)
                                        with tag('td'):
                                            with tag('strong'):
                                                text('Magnification: ')
                                            text(magnification)
                                        with tag('td'):
                                            with tag('strong'):
                                                text('Resolution: ')
                                            text('{} x {}'.format(
                                                width, height))
                                    with tag('tr'):
                                        with tag('td'):
                                            with tag('strong'):
                                                text('Spot size: ')
                                            text(spotsize)
                                        with tag('td'):
                                            with tag('strong'):
                                                text('Detector: ')
                                            text(detector)
                                        with tag('td'):
                                            with tag('strong'):
                                                text('Vacuum: ')
                                            text(vacuum)
                                        with tag('td'):
                                            with tag('strong'):
                                                text('User text: ')
                                            text(user_text)
                                        with tag('td'):
                                            with tag('strong'):
                                                text('Filename: ')
                                            text(os.path.split(image)[-1])

        else:
            with tag('h2'):
                text('No samples found')
                doc.asis('<hr>')

        # connect to the elog
        log = elog.open(hostname=elog_hostname,
                        port=elog_port,
                        user=elog_user,
                        password=elog_password,
                        use_ssl=elog_use_ssl,
                        logbook=self.elog_logbook)

        # search for a logbook entries with the same protocol
        protocol_ids = log.search({'Protocol ID': self.protocol})
        if (len(protocol_ids)) > 1:
            # there are more than 1 entry with this protocol ID. It is a problem. Ask the user what to do.
            # TODO: implement this situation
            raise error

        # until we don't discover how to remove the attachments, we have to cancel the whole message
        if protocol_ids:
            log.delete(protocol_ids[0])

        self.attributes = {
            'Protocol ID': self.protocol,
            'Project': self.project,
            'Customer': self.customer,
            'Operator': 'Logbook robot',
            'Creation date': datetime.today().timestamp()
        }

        self.message = doc.getvalue()
        # post the log entry
        log.post(self.message, reply=False, attributes=self.attributes,
                 attachments=self.pdf_reports, encoding=elog_encoding)

        self.filelist_scrolltext.insert(
            END, 'Logbook entry successfully generated and submitted\n')


#
# Automatic Logbook
#
class AutomaticLogbook(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Automatic Logbook")
        mainframe = ttk.Frame(self)
        mainframe.grid(padx=20, pady=20)
        quattro_button = ttk.Button(mainframe, text="SEM Quattro", command=lambda: QuattroLogbook(
            self)).grid(column=0, row=1, padx=10, pady=5, sticky="ew")
        ttk.Button(mainframe, text="Button1").grid(
            column=1, row=1, padx=10, pady=5, sticky="ew")
        ttk.Button(mainframe, text="Button2").grid(
            column=0, row=2, padx=10, pady=5, sticky="ew")
        ttk.Button(mainframe, text="Button2").grid(
            column=1, row=2, padx=10, pady=5, sticky="ew")

        # close button
        ttk.Button(mainframe, text="Close", command=self.destroy).grid(
            column=0, row=4, columnspan=2, padx=5, pady=5, sticky="ew")

#
# ExtractPicsFromXLS
#


class ExtractPicsFromXLS(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.filenames = []
        self.title("Pictures extractor")
        mainframe = ttk.Frame(self)
        mainframe.grid(padx=20, pady=20)
        ttk.Label(mainframe, text="Picture extraction from XLS files", font=(
            "Arial", 24)).grid(column=0, row=0, padx=20, pady=20, columnspan=3, sticky="EW")
        ttk.Label(mainframe, text="Use this tool to extract images from MS Excel files and save them on your disk as PNG. Select one or more files and then click of start.").grid(
            column=0, row=1, padx=5, pady=5, columnspan=3, sticky="EW")
        # ttk.Label(mainframe, text ="List of selected files").grid(column=0, row=2, padx=0, pady=0, columnspan=1, sticky="EW")
        self.filelist_scrolltext = scrolledtext.ScrolledText(
            mainframe, width=40, height=10)
        self.filelist_scrolltext.grid(
            column=0, row=3, padx=20, pady=20, columnspan=3, sticky="EW")
        self.filelist_scrolltext.insert(
            END, "List of files to be processed...\n")

        # add files button
        add_files_button = ttk.Button(
            mainframe, text="Add files...", command=self.get_filenames)
        add_files_button.grid(column=0, row=4, padx=5, pady=5, sticky="ew")

        # process files
        process_files_button = ttk.Button(
            mainframe, text="Process files", command=self.process_files)
        process_files_button.grid(column=1, row=4, padx=5, pady=5, sticky="ew")

        # close button
        ttk.Button(mainframe, text="Close", command=self.destroy).grid(
            column=2, row=4, columnspan=1, padx=5, pady=5, sticky="ew")

    def process_files(self):
        if self.filenames:
            self.filelist_scrolltext.insert(
                END, "Processing " + str(len(self.filenames)) + " files...\n")
            self.filelist_scrolltext.insert(END, "Opening Excel...")
            excel = win32.gencache.EnsureDispatch('Excel.Application')
            self.filelist_scrolltext.insert(END, " done\n")
            for file in self.filenames:
                self.filelist_scrolltext.insert(
                    END, "Processing file: " + file + "\n")
                basefilename = os.path.splitext(file)[0]
                wb = excel.Workbooks.Open(file, ReadOnly=True)
                for sheet in wb.Worksheets:
                    for i, shape in enumerate(sheet.Shapes):
                        if shape.Name.startswith('Picture') or shape.Name.endswith('.png'):
                            shape.Copy()
                            image = ImageGrab.grabclipboard()
                            output_filename = basefilename + '_' + \
                                sheet.Name.replace(
                                    " ", "_") + '_' + shape.Name.replace(" ", "_") + '.png'
                            image.save(output_filename)
                            self.filelist_scrolltext.insert(
                                END, "Saving image: " + output_filename + "\n")
            self.filelist_scrolltext.insert(END, "Extraction completed!\n")
            self.filenames = []
        else:
            self.filelist_scrolltext.insert(
                END, "No files selected. Please use the add files button to add at least one file.\n")

    def get_filenames(self):

        new_filenames = filedialog.askopenfilename(
            parent=self, title="Select one or more xls files", multiple=True, filetypes=[("MS Excel", "*.xl*")])
        if new_filenames:
            self.filenames.extend(new_filenames)
            for filename in new_filenames:
                self.filelist_scrolltext.insert(END, filename + '\n')


#
# main application
#
class MainApp(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("labtools v3")
        self.parent.resizable(width=False, height=False)
        # self.parent.geometry("480x320")
        mainframe = ttk.Frame(self)

        mainframe.grid(padx=20, pady=20)
        ttk.Label(mainframe, text="Welcome to labtools", font=("Arial", 24)).grid(
            column=0, row=0, padx=20, pady=40, columnspan=2, sticky="EW")

        extract_pics_from_xls_button = ttk.Button(mainframe, text="Extract pics from xls", command=lambda: ExtractPicsFromXLS(
            self)).grid(column=0, row=1, padx=10, pady=5, sticky="ew")

        convert_bmp_to_png_button = ttk.Button(mainframe, text="Convert BMPs to PNGs", command=lambda: ConvertBMPtoPNG(
            self)).grid(column=1, row=1, padx=10, pady=5, sticky="ew")

        remove_databar_button = ttk.Button(mainframe, text="Remove databar from TIFF", command=lambda: RemoveDatabarFromTIF(
            self)).grid(column=0, row=2, padx=10, pady=5, sticky="ew")

        auto_logbook_quattro_button = ttk.Button(mainframe, text="Prepare automatic logbook entries", command=lambda: AutomaticLogbook(
            self)).grid(column=1, row=2, padx=10, pady=5, sticky="ew")

        for i in range(0, 2):
            for j in range(2, 5):
                ttk.Button(mainframe, text="Button " + str(i) + ", " + str(j)
                           ).grid(column=i, row=j + 1, padx=10, pady=5, sticky="ew")

        ttk.Button(mainframe, text="Close", command=self.parent.destroy).grid(
            column=0, row=6, columnspan=2, padx=20, pady=20, sticky="ew")


#
# define root element and start application
#
def main():
    root = ttk.Tk()
    app = MainApp(root)
    app.grid()
    root.mainloop()


#
# start if called from command line
#
if __name__ == '__main__':
    main()
