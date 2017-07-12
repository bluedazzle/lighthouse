# coding: utf-8

from __future__ import unicode_literals
from django.contrib.sitemaps import Sitemap
from core.models import ZHArticle


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    limit = 1000

    def items(self):
        objects = ZHArticle.objects.all()
        return objects

    def lastmod(self, item):
        return item.create_time

    def location(self, item):
        return r'/article/{0}'.format(item.token)
