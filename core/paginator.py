# coding: utf-8
from __future__ import unicode_literals

from django.core.paginator import Paginator
from django.core.cache import cache
from sqlalchemy import func

from lg_data.db.models import DBSession, ZHArticle
from lg_data.utils import md5
from lighthouse.core.models import ZHArticle as DZHArticle


class RedisCachePaginator(Paginator):
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, *args, **kwargs):
        self.session = DBSession()
        super(RedisCachePaginator, self).__init__(object_list, per_page, orphans, allow_empty_first_page)

    def _get_count(self):
        """
        Returns the total number of objects, across all pages.
        """
        if self._count is None:
            count = cache.get('article_count')
            if count:
                self._count = count
                return self._count
            q = self.session.query(ZHArticle)
            self._count = self.get_count_from_db(q)
            cache.set('article_count', self._count, 60 * 60 * 6)
        return self._count

    count = property(_get_count)

    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.
        """
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        self.object_list = DZHArticle.objects.raw(
            '{0} OFFSET {1} LIMIT {2}'.format(self.object_list.raw_query, bottom, self.per_page))
        return self._get_page(self.object_list, number, self)

    def get_count_from_db(self, q):
        count_q = q.statement.with_only_columns([func.count()])
        count = q.session.execute(count_q).scalar()
        return count


class SearchPaginator(RedisCachePaginator):
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, *args, **kwargs):
        self.keyword = kwargs.get('keyword', '')
        self.session = DBSession()
        super(SearchPaginator, self).__init__(object_list, per_page, orphans, allow_empty_first_page)

    def _get_count(self):
        """
        Returns the total number of objects, across all pages.
        """
        key = '{0}_article_count'.format(md5(self.keyword.encode('utf-8')))
        if self._count is None:
            count = cache.get(key)
            if count:
                self._count = count
                return self._count
            self._count = self.session.execute(
                '''select count(title) from core_zharticle where title ~ '{keyword}';'''.format(
                    keyword=self.keyword)).first()[0]
            cache.set(key, self._count, 60 * 5)
        return self._count

    count = property(_get_count)
