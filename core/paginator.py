from django.core.paginator import Paginator
from django.core.cache import cache


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
