# coding: utf-8
from __future__ import unicode_literals

from django.core.paginator import Paginator
from django.core.cache import cache

from lg_data.db.models import DBSession
from lg_data.utils import md5


class RedisCachePaginator(Paginator):
    def _get_count(self):
        """
        Returns the total number of objects, across all pages.
        """
        if self._count is None:
            count = cache.get('article_count')
            if count:
                self._count = count
                return self._count
            try:
                self._count = self.object_list.count()
            except (AttributeError, TypeError):
                # AttributeError if object_list has no count() method.
                # TypeError if object_list.count() requires arguments
                # (i.e. is of type list).
                self._count = len(self.object_list)
            cache.set('article_count', self._count, 60 * 60 * 6)
        return self._count

    count = property(_get_count)


class SearchPaginator(Paginator):
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
            try:
                self._count = self.session.execute(
                    '''select count(title) from core_zharticle where title ilike '%{keyword}%';'''.format(
                        keyword=self.keyword)).first()[0]
            except (AttributeError, TypeError):
                # AttributeError if object_list has no count() method.
                # TypeError if object_list.count() requires arguments
                # (i.e. is of type list).
                self._count = len(self.object_list)
            cache.set(key, self._count, 60 * 5)
        return self._count

    count = property(_get_count)
