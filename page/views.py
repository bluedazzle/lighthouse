# coding: utf-8
from __future__ import unicode_literals

from django.views.generic import DetailView
from django.views.generic import ListView

from core.models import ZHArticle


class IndexView(ListView):
    model = ZHArticle
    template_name = 'index.html'
    paginate_by = 50
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
        from bs4 import BeautifulSoup
        import jieba.analyse
        obj = context['zharticle']
        soup = BeautifulSoup(obj.content)
        raw_text = soup.get_text()
        summary = raw_text[:200]
        title_list = [itm for itm in jieba.cut(obj.title) if len(itm) > 1]
        seg_list = jieba.analyse.extract_tags(raw_text, topK=100, withWeight=False)
        seg_list = seg_list[:20]
        seg_list.extend(title_list)
        seg_list = set(seg_list)
        keywords = ','.join(seg_list)
        return super(ArticleDetailView, self).render_to_response(context, **response_kwargs)
