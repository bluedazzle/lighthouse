from django.conf.urls import include, url
from page.views import *

urlpatterns = [
    # Examples:
    url(r'^article/(?P<slug>([a-z0-9-])+)/$', ArticleDetailView.as_view()),
    url(r'^$', IndexView.as_view()),

    # url(r'^blog/', include('blog.urls')),

]
