# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 08:32:34 2022

@author: Antonio
"""

import configparser
from pathlib import Path

import tifffile
from PIL import Image


def main():
    img = Path('fei.tif')
    with Image.open(img) as sourceimg:

        tiffinfo = sourceimg.tag_v2

        # check if the user comment is there
        # code 37510
        tiffinfo[37510] = '1500'
        sourceimg.save(img, tiffinfo=tiffinfo)

    with Image.open(img) as sourceimg:
        tiffinfo = sourceimg.tag_v2
        # rint(tiffinfo[34682])
        with open('feitag.txt', 'w') as txt:
            txt.write(tiffinfo[34682])
        conf = configparser.ConfigParser(allow_no_value=True)
        conf.read_string(tiffinfo[34682])
        print(conf['Scan']['PixelWidth'])
    # with tifffile.TiffFile(micro_pic_path) as tif:
    #     for page in tif.pages:
    #         for tag in page.tags:
    #             tag_name, tag_value = tag.name, tag.value
    #             print(f'{tag_name} --> {tag_value}')

    #     print(tifffile.TIFF.TAGS[37510])
    #     if tifffile.TIFF.TAGS[37510] in tif.pages[0].tags:
    #         user_comment_tag = tif.pages[0].tags[tifffile.TIFF.TAGS[37510]]
    #         print(user_comment_tag.value)
    #     else:
    #         user_comment_tag = tifffile.TiffTag(out,)
    #     # page = tif.pages[0]
    #     # print(page.tags['FEI_HELIOS']._astuple())
    #     # for tag in page.tags:
    #     #     print(tag.astuple(tif))

    #     # if 'ImageUniqueID' not in page.tags:

    #     #     tifffile.TiffTag(parent, offset, code, dtype, count, value, valueoffset)
    #     # #print(page.tags['ImageUniqueID']).value


if __name__ == '__main__':
    main()
