from __future__ import unicode_literals
from django.db import models


# Create your models here.

class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Proxy(BaseModel):
    proxy_choices = (
        (1, 'HTTP'),
        (2, 'HTTPS'),
    )
    host = models.GenericIPAddressField()
    port = models.IntegerField(default=8080)
    protocol = models.IntegerField(default=1, choices=proxy_choices)
    available = models.BooleanField(default=True)

    def __unicode__(self):
        return '{0}:{1}'.format(self.host, self.port)

    def __repr__(self):
        return '{0}:{1}'.format(self.host, self.port)


class ZHUser(BaseModel):
    hash = models.CharField(max_length=64, unique=True)
    zuid = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=256, default='')
    avatar = models.CharField(max_length=512, default='')
    link = models.CharField(max_length=512, default='')
    slug = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=512, default='', null=True, blank=True)
    headline = models.CharField(max_length=128, default='', null=True, blank=True)
    crawl_column = models.BooleanField(default=False)
    crawl_follow = models.BooleanField(default=False)

    def __unicode__(self):
        return '{0}|{1}'.format(self.name, self.slug)


class ZHColumn(BaseModel):
    name = models.CharField(max_length=256, default='')
    link = models.CharField(max_length=512, default='')
    hash = models.CharField(max_length=64, unique=True)
    slug = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=512, default='', null=True, blank=True)
    avatar = models.CharField(max_length=512, default='')
    creator = models.ForeignKey(ZHUser, related_name='zhuser_columns', null=True, blank=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return '{0}-{1}'.format(self.name, self.slug)


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name


class ZHArticle(BaseModel):
    title = models.CharField(max_length=512)
    link = models.CharField(max_length=512)
    md5 = models.CharField(max_length=64, unique=True)
    content = models.TextField(default='')
    summary = models.TextField(default='')
    cover = models.CharField(max_length=512)
    token = models.CharField(max_length=16, unique=True)
    author = models.ForeignKey(ZHUser, related_name='zhuser_articles', null=True, blank=True, on_delete=models.SET_NULL)
    belong = models.ForeignKey(ZHColumn, related_name='column_articles', null=True, blank=True,
                               on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, related_name='tag_articles')

    def __unicode__(self):
        return '{0}-{1:%Y-%m-%d %H:%M:%S}'.format(self.title, self.create_time)


class ZHRandomColumn(BaseModel):
    slug = models.CharField(max_length=100, unique=True)
    link = models.CharField(max_length=512)
    hash = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.slug
