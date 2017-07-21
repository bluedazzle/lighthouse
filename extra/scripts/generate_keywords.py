# coding: utf-8
from __future__ import unicode_literals

import logging
import sys
import os
import math
import jieba.analyse

from bs4 import BeautifulSoup
from sqlalchemy import func

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)


def generate_keywords(obj):
    soup = BeautifulSoup(obj.content, "lxml")
    raw_text = soup.get_text()
    obj.summary = "".join(raw_text[:200].split())
    title_list = [itm for itm in jieba.cut(obj.title) if len(itm) > 1]
    seg_list = jieba.analyse.extract_tags(raw_text, topK=100, withWeight=False)
    seg_list = seg_list[:20]
    seg_list.extend(title_list)
    seg_list = set(seg_list)
    obj.keywords = ','.join(seg_list)


def iter_all_data(exist=None):
    from lg_data.db.models import ZHArticle, DBSession
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
            logging.info('Current {0} {1}/{2} {3}%'.format(article.token, count+1, total, (count+1.0) / total * 100))
            generate_keywords(article)
            count += 1
            try:
                session.commit()
            except Exception as e:
                logging.exception('ERROR in commit data {0} reason: {1}'.format(article, e))
                session.rollback()
                fail_list.append(article.id)
    logging.info('generate keywords down, fail: {0}'.format(fail_list))


if __name__ == '__main__':
    iter_all_data(326868)


