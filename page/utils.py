# coding: utf-8
from __future__ import unicode_literals

import logging

SIZE_SMALL = 's'
SIZE_MEDIUM = 'm'
SIZE_LARGE = 'l'
SIZE_BIG = 'b'
SIZE_RAW = 'r'


def convert_image_size(url, size=SIZE_BIG):
    try:
        url_list = url.split('.')
        image = '.'.join(url_list[:-1])
        ext = url_list[-1]
        new_url = '{0}{1}.{2}'.format(image[:-1], size, ext)
        return new_url
    except Exception as e:
        logging.exception('Convert image size error, url: {0} reason: {1}'.format(url, e))
        return url
