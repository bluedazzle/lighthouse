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


class ZHArticle(BaseModel):
    title = models.CharField(max_length=512)
    link = models.CharField(max_length=512)
    md5 = models.CharField(max_length=64, unique=True)
    content = models.TextField(default='')
    summary = models.TextField(default='')
    cover = models.CharField(max_length=512)
    token = models.CharField(max_length=16, unique=True)

    def __unicode__(self):
        return self.title
