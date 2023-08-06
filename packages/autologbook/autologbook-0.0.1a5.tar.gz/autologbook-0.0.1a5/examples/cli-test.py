# -*- coding: utf-8 -*-
"""
Created on Fri May 20 08:38:05 2022

@author: elog-admin
"""

import argparse
from pathlib import Path


def main():

    parser = argparse.ArgumentParser(description='Check path')
    parser.add_argument('path', help='path to the file', type=Path)

    args = parser.parse_args()

    # with args.path.open('w') as file:
    #     file.write(str(args.path))

    # print(str(args.path))

    # file = R:\A226\Results\2022\12456-RADCAS-Bulgheroni
    # uri = https://10.166.16.24/micro/2022/12456-RADCAS-Bulgheroni/

    path = args.path  # Path("R:\A226\Results\2022\123456-RADCAS-Bulgheroni")
    for part in path.parts:
        print(part)
    index = path.parts.index('Results')
    new_path = Path('micro').joinpath(*path.parts[index + 1:])
    new_uri = 'https://10.166.16.24/' + str(new_path).replace('\\', '/')
    print(str(new_uri))


if __name__ == '__main__':
    main()
