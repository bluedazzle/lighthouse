# coding: utf-8
from __future__ import unicode_literals

import six

from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView

from core.models import ZHArticle, ZHColumn
from core.paginator import RedisCachePaginator
from page.utils import convert_image_size

from core.mixin.seo import HostMixin

from lighthouse.core.paginator import SearchPaginator


class ArticleListView(HostMixin, ListView):
    model = ZHArticle
    template_name = 'index.html'
    paginate_by = 10
    http_method_names = ['get']
    ordering = '-create_time'
    paginator_class = RedisCachePaginator
    keyword = None

    @staticmethod
    def change_cover_size(obj_list):
        for obj in obj_list:
            obj.cover = convert_image_size(obj.cover)
        return obj_list

    def get_queryset(self):
        self.keyword = self.request.GET.get('s', None)
        if self.keyword:
            queryset = ZHArticle.objects.raw('''SELECT title, md5, cover, token, belong_id, core_zhcolumn.id, core_zharticle.create_time, name, hash, slug, avatar
            FROM core_zharticle
            LEFT OUTER JOIN core_zhcolumn
            ON (belong_id = core_zhcolumn.id)
            WHERE title ~ '{keyword}')
            ORDER BY core_zharticle.create_time DESC'''.format(keyword=self.keyword))
            self.paginator_class = SearchPaginator
        else:
            queryset = ZHArticle.objects.raw('''SELECT title, md5, cover, token, belong_id, core_zhcolumn.id, core_zharticle.create_time, name, hash, slug, avatar
            FROM core_zharticle
            LEFT OUTER JOIN core_zhcolumn
            ON (belong_id = core_zhcolumn.id)
            ORDER BY core_zharticle.create_time DESC''')
        return queryset

    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_empty_first_page=True, **kwargs):
        if self.keyword:
            kwargs['keyword'] = self.keyword
        return self.paginator_class(
            queryset, per_page, orphans=orphans,
            allow_empty_first_page=allow_empty_first_page, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if self.keyword:
            context['search'] = self.keyword
        context['zharticle_list'] = self.change_cover_size(context['zharticle_list'])
        page_obj = context['page_obj']
        end = page_obj.number + 5
        if end > page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        context['page_range'] = page_obj.paginator.page_range[page_obj.number - 1:end]
        return super(ArticleListView, self).render_to_response(context, **response_kwargs)


class ArticleDetailView(HostMixin, DetailView):
    model = ZHArticle
    slug_field = 'token'
    slug_url_kwarg = 'slug'
    http_method_names = ['get']
    template_name = 'article_detail.html'

    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.
        Note that this method is called by the default implementation of
        `get_object` and may not be called if `get_object` is overridden.
        """
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.select_related('belong').select_related('author').only('title',
                                                                                                          'cover',
                                                                                                          'create_time',
                                                                                                          'link',
                                                                                                          'content',
                                                                                                          'summary',
                                                                                                          'keywords',
                                                                                                          'author__avatar',
                                                                                                          'author__link',
                                                                                                          'author__name',
                                                                                                          'belong__avatar',
                                                                                                          'belong__name').all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )
        return self.queryset.all()

    @staticmethod
    def change_cover_size(obj_list):
        for obj in obj_list:
            obj.cover = convert_image_size(obj.cover)
        return obj_list

    def generate_relate_articles(self, context):
        if self.object.belong:
            context['relate_list'] = self.change_cover_size(
                self.object.belong.column_articles.select_related('belong').select_related('author').only('title',
                                                                                                          'cover',
                                                                                                          'create_time',
                                                                                                          'token',
                                                                                                          'summary',
                                                                                                          'author__avatar',
                                                                                                          'author__link',
                                                                                                          'author__name',
                                                                                                          'belong__avatar',
                                                                                                          'belong__name').exclude(
                    id=self.object.id).order_by(
                    '-create_time')[:3])
        context['recommand_list'] = self.change_cover_size(
            ZHArticle.objects.select_related('belong').select_related('author').only('title',
                                                                                     'cover',
                                                                                     'create_time',
                                                                                     'token',
                                                                                     'summary',
                                                                                     'author__avatar',
                                                                                     'author__link',
                                                                                     'author__name',
                                                                                     'belong__avatar',
                                                                                     'belong__name').all().order_by(
                '-create_time')[:3])

    def render_to_response(self, context, **response_kwargs):
        self.generate_relate_articles(context)
        return super(ArticleDetailView, self).render_to_response(context, **response_kwargs)


class ColumnDetailView(HostMixin, ListView):
    model = ZHArticle
    template_name = 'column.html'
    column = None
    paginate_by = 10

    @staticmethod
    def change_cover_size(obj_list):
        for obj in obj_list:
            obj.cover = convert_image_size(obj.cover)
        return obj_list

    def get_column_info(self, slug):
        if not slug:
            raise Http404
        self.column = get_object_or_404(ZHColumn, slug=slug)

    def get(self, request, *args, **kwargs):
        self.get_column_info(kwargs.get('slug'))
        return super(ColumnDetailView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return self.column.column_articles.order_by('-create_time').all()

    def render_to_response(self, context, **response_kwargs):
        context['column'] = self.column
        context['object_list'] = self.change_cover_size(context['object_list'])
        page_obj = context['page_obj']
        end = page_obj.number + 5
        if end > page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        context['page_range'] = page_obj.paginator.page_range[page_obj.number - 1:end]
        return super(ColumnDetailView, self).render_to_response(context, **response_kwargs)
