# coding: utf-8
from __future__ import unicode_literals

import random
import logging
import sys
import os
import math

from sqlalchemy import func

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)


def fix_image_in_article(exist=None):
    from models import ZHArticle, DBSession
    from bs4 import BeautifulSoup
    session = DBSession()
    fail_list = []
    limit = 1000
    total = session.query(func.count(ZHArticle.id)).scalar()
    total_offset = int(math.ceil(total / float(limit)))
    if exist:
        start = exist / limit
        count = start * limit - 1
    else:
        start = 1
        count = 0
    for i in xrange(start, total_offset):
        offset = limit * i
        result = session.query(ZHArticle).order_by('id').limit(limit).offset(offset).all()

        for article in result:
            logging.info(
                'Current {0} {1}/{2} {3}%'.format(article.token, count + 1, total, (count + 1.0) / total * 100))
            soup = BeautifulSoup(article.content)
            finds = soup.find_all('img')
            for itm in finds:
                host_random = random.randint(1, 4)
                itm['src'] = 'https://pic{0}.zhimg.com/{1}'.format(host_random, itm['src'])
            if not article.cover:
                if finds:
                    article.cover = finds[0]['src']
            article.content = soup.prettify()
            count += 1
            try:
                session.commit()
            except Exception as e:
                logging.exception('ERROR in commit data {0} reason: {1}'.format(article, e))
                session.rollback()
                fail_list.append(article.id)
    logging.info('fix image down, fail: {0}'.format(fail_list))


if __name__ == '__main__':
    fix_image_in_article(337441)
