# coding: utf-8
from __future__ import unicode_literals

import six

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.views.generic import DetailView
from django.views.generic import ListView

from core.models import ZHArticle, ZHColumn
from core.paginator import RedisCachePaginator
from page.utils import convert_image_size


class ArticleListView(ListView):
    model = ZHArticle
    template_name = 'index.html'
    paginate_by = 10
    http_method_names = ['get']
    ordering = '-create_time'
    paginator_class = RedisCachePaginator

    @staticmethod
    def change_cover_size(obj_list):
        for obj in obj_list:
            obj.cover = convert_image_size(obj.cover)
        return obj_list

    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.select_related('belong').defer('content', 'summary', 'modify_time', 'link',
                                                                   'keywords').all()
        elif self.model is not None:
            queryset = self.model._default_manager.select_related('belong').defer('content', 'summary', 'modify_time',
                                                                                  'link',
                                                                                  'keywords').all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
        queryset = queryset.order_by(*ordering)
        return queryset

    def render_to_response(self, context, **response_kwargs):
        context['zharticle_list'] = self.change_cover_size(context['zharticle_list'])
        page_obj = context['page_obj']
        end = page_obj.number + 5
        if end > page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        context['page_range'] = page_obj.paginator.page_range[page_obj.number - 1:end]
        return super(ArticleListView, self).render_to_response(context, **response_kwargs)


class ArticleDetailView(DetailView):
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
        # self.generate_relate_articles(context)
        return super(ArticleDetailView, self).render_to_response(context, **response_kwargs)
