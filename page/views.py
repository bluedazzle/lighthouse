# coding: utf-8
from __future__ import unicode_literals

from django.views.generic import DetailView
from django.views.generic import ListView

from core.models import ZHArticle


class IndexView(ListView):
    model = ZHArticle
    template_name = 'index.html'
    paginate_by = 10
    http_method_names = ['get']
    ordering = '-create_time'

    def render_to_response(self, context, **response_kwargs):
        return super(IndexView, self).render_to_response(context, **response_kwargs)


class ArticleDetailView(DetailView):
    model = ZHArticle
    slug_field = 'token'
    slug_url_kwarg = 'slug'
    http_method_names = ['get']
    template_name = 'article_detail.html'

    def render_to_response(self, context, **response_kwargs):
        obj = context['zharticle']
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(obj.content)
        finds = soup.find_all('img')
        for itm in finds:
            itm['src'] = 'https://pic4.zhimg.com/{0}'.format(itm['src'])
        obj.content = soup.prettify()
        return super(ArticleDetailView, self).render_to_response(context, **response_kwargs)
