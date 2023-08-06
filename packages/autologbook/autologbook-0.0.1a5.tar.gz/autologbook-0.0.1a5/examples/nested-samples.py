# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 09:07:05 2022

@author: elog-admin
"""

from pathlib import Path


def main():

    newimage = Path(
        'R:/A226/Results/2022/123 - proj - resp/SampleA/SubSampleB/SubSampleC/D/D3/image.tiff')
    monitor = Path('R:/A226/Results/2022/123 - proj - resp/')

    # get the subtree between the newimage_path and the monitored path
    subtree = newimage.relative_to(monitor)

    print(f'subtree is {subtree}')

    parents_list = []
    for i in range(len(subtree.parents[0].parts)):
        if i == 0:
            parents_list.append((subtree.parents[0].parts[i], None))
        else:
            parents_list.append((subtree.parents[0].parts[i],
                                 subtree.parents[0].parts[i - 1]))

    for pair in parents_list:
        print(pair)


if __name__ == '__main__':
    main()
