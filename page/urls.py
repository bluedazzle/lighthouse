from django.conf.urls import include, url
from page.views import *

urlpatterns = [
    # Examples:
    url(r'^article/(?P<slug>([a-z0-9-])+)/$', ArticleDetailView.as_view(), name='article'),
    url(r'^column/(?P<slug>([a-zA-Z0-9-_])+)/$', ColumnDetailView.as_view(), name='column'),
    url(r'^articles/$', ArticleListView.as_view(), name='articles'),
    url(r'^$', ArticleListView.as_view()),

    # url(r'^blog/', include('blog.urls')),

]