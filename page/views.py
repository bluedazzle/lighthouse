# coding: utf-8
from __future__ import unicode_literals

from django.views.generic import DetailView
from django.views.generic import ListView

from core.models import ZHArticle, ZHColumn
from page.utils import convert_image_size


class ArticleListView(ListView):
    model = ZHArticle
    template_name = 'index.html'
    paginate_by = 10
    http_method_names = ['get']
    ordering = '-create_time'

    @staticmethod
    def change_cover_size(obj_list):
        for obj in obj_list:
            obj.cover = convert_image_size(obj.cover)
        return obj_list

    def get_queryset(self):
        queryset = super(ArticleListView, self).get_queryset()
        queryset = queryset.defer('content', 'summary', 'modify_time', 'link', 'keywords')
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

    @staticmethod
    def change_cover_size(obj_list):
        for obj in obj_list:
            obj.cover = convert_image_size(obj.cover)
        return obj_list

    def generate_relate_articles(self, context):
        if self.object.belong:
            context['relate_list'] = self.change_cover_size(
                self.object.belong.column_articles.exclude(id=self.object.id).order_by('-create_time')[:3])
        context['recommand_list'] = self.change_cover_size(ZHArticle.objects.all().order_by('-create_time')[:3])

    def render_to_response(self, context, **response_kwargs):
        self.generate_relate_articles(context)
        return super(ArticleDetailView, self).render_to_response(context, **response_kwargs)
