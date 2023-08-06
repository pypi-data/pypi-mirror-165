# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 15:33:17 2022

@author: elog-admin
"""
import argparse
import datetime
import random
import shutil
import sys
import time
from pathlib import Path


def main_parser():
    """
    Define the main argument parser.

    Returns
    -------
    parser : ArgumentParser
        The main parser.
    """
    parser = argparse.ArgumentParser(description='''
                                 Test your autologbook generating fake analysis
                                 ''')
    parser.add_argument('-m', '--microscope', type=str, dest='microscope',
                        choices=('Quattro', 'Versa'), default='Quattro',
                        help='''
                        Set the microscope for which the fake analysis will
                        be generated.
                        ''')
    parser.add_argument('-d', '--delay-avg', type=float, dest='delay_mu',
                        default=5, help='''
                        The average delay in seconds between the generation of two
                        following events.
                        '''
                        )
    parser.add_argument('-s', '--delay-sigma', type=float, dest='delay_sigma',
                        default=1, help='''
                        The spread delay in seconds between the generation of two
                        following events.
                        '''
                        )
    parser.add_argument('-n', '--num-events', type=int, dest='number_events',
                        default=100, help='''
                        The total number of events to be generated.
                        '''
                        )
    parser.add_argument('--subsamples', action='store_const', const=True, default=False, dest='subsamples',
                        help='Requires nested samples')

    parser.add_argument('--singlesample', action='store_const', const=True, default=False, dest='singlesample',
                        help='Use only one sample')

    parser.add_argument('--no-mirroring', action='store_const', const=True, default=False, dest='no_mirroring',
                        help='If selected, files are created directly to the R folder. '
                        'The autologbook has to run without mirroring engine.')

    parser.add_argument('--only-creation', action='store_const', const=True, default=False, dest='only_creation',
                        help='If selected, elements will be added but never removed.')

    parser.add_argument('--allow-duplicated-ID', action='store_const', const=True, default=False,
                        dest='duplicateID', help='If selected, microscope pictures with duplicated ID will be created.')

    parser.add_argument('--allow-missing-ID', action='store_const', const=True, default=False, dest='missingID',
                        help='If selected, 1 out of 3 microscope pictures with be saved without ID')

    return parser


def main(cli_args, prog):

    parser = main_parser()
    if prog:
        parser.prog = prog

    args = parser.parse_args(cli_args)

    microscope = args.microscope

    if microscope == 'Quattro':
        input_tifffile = Path('S:/software-dev/myquattro.tif')
        dest_folder_mirroring = Path(
            'C:/Users/elog-admin/Documents/src/12456-RADCAS-Bulgheroni')
        dest_folder_nomirroring = Path(
            'R:/A226/Results/2022/12456-RADCAS-Bulgheroni/')
    elif microscope == 'Versa':
        input_tifffile = Path('S:/software-dev/myversa.tif')
        dest_folder_mirroring = Path(
            'C:/Users/elog-admin/Documents/src/#12457-FIBVERSA-Bulgheroni')
        dest_folder_nomirroring = Path(
            'R:/A226/Results/2022/12457-FIBVERSA-Bulgheroni')

    dest_folder = dest_folder_mirroring
    if args.no_mirroring:
        dest_folder = dest_folder_nomirroring

    delay_mu = args.delay_mu
    delay_sigma = args.delay_sigma

    events_only_creation = ('new_pic', 'new_pic')
    events = ('new_pic', 'remove_pic', 'new_pic')
    if args.only_creation:
        events = events_only_creation

    samples_with_subsamples = (Path('Graphite'),
                               Path('Graphite/Nera'),
                               Path('Graphite/Polvere fine'),
                               Path('Cemento'),
                               Path('Cemento/baritico'),
                               Path('Carta'),
                               Path('Carta/Cartolina'),
                               Path('Carta/Cartolina/Firenze'),
                               Path('Carta/Scatolone')
                               )

    single_sample = (Path('Graphite'),)

    samples_without_subsamples = (Path('Graphite'),
                                  Path('Cemento'),
                                  Path('Carta')
                                  )
    missingID = (False, False, False)
    if args.missingID:
        missingID = (True, False, False)

    samples = samples_without_subsamples
    if args.subsamples:
        samples = samples_with_subsamples

    if args.singlesample:
        samples = single_sample

    for sample in samples:
        (dest_folder / sample).mkdir(exist_ok=True)

    print(f'| Waiting {len(samples)} s before continuing')
    time.sleep(len(samples))

    number_events = args.number_events

    for i in range(number_events):
        if args.duplicateID:
            j = random.randint(0, int(number_events / 4))
        else:
            j = i
        event = events[random.randint(0, len(events) - 1)]
        sample = samples[random.randint(0, len(samples) - 1)]
        missing = missingID[random.randint(0, len(missingID) - 1)]
        ts = datetime.datetime.now()
        if microscope == 'Quattro':
            if missing:
                dest_file = dest_folder / sample / \
                    Path(
                        f'{str(input_tifffile.stem)}_{ts:%H%M%S}{str(input_tifffile.suffix)}')
            else:
                dest_file = dest_folder / sample / \
                    Path(
                        f'{j:03}-{str(input_tifffile.stem)}_{ts:%H%M%S}{str(input_tifffile.suffix)}')
        elif microscope == 'Versa':
            if missing:
                dest_file = dest_folder / sample / \
                    Path(
                        f'{ts:%H%M%S}_{str(input_tifffile.stem)}{str(input_tifffile.suffix)}')
            else:
                dest_file = dest_folder / sample / \
                    Path(
                        f'{ts:%H%M%S}_{str(input_tifffile.stem)}_{j:03}{str(input_tifffile.suffix)}')
        delay = random.gauss(delay_mu, delay_sigma)
        while delay <= 0:
            delay = random.gauss(delay_mu, delay_sigma)
        time.sleep(delay)
        if event == 'new_pic':
            print(
                f'| {i:03} | {event:<10} | {str(sample):<40} | {str(dest_file.name):<25} |')
            # print(
            #    f'Iteration {i:03} of type {event} on {sample} file {dest_file.name} with {delay:.3f} sec delay')
            shutil.copy(str(input_tifffile), str(dest_file))
        elif event == 'remove_pic':
            for file in (dest_folder / sample).glob('*tif*'):
                file.unlink()
                print(
                    f'| {i:03} | {event:<10} | {str(sample):<40} | {str(file.name):<25} |')
                # print(
                #     f'Iteration {i:03} of type {event} on {sample} file {file.name} with {delay:.3f} sec delay')
                break
        elif event == 'mod_pic':
            for file in (dest_folder / sample).glob('*tif*'):
                file.touch()
                print(
                    f'| {i:03} | {event:<10} | {str(sample):<40} | {str(file.name):<25} |')
                # print(
                #     f'Iteration {i:03} of type {event} on {sample} file {file.name} with {delay:.3f} sec delay')
                break


if __name__ == '__main__':
    main(sys.argv[1:], 'py test-stability.py')
