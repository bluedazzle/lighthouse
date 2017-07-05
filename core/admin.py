from django.contrib import admin
from django.forms import ModelForm

from core.models import *


# Register your models here.

class AritcleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AritcleForm, self).__init__(*args, **kwargs)
        if self.instance.author:
            self.fields['author'].queryset = ZHUser.objects.filter(id=self.instance.author.id)
        if self.instance.belong:
            self.fields['belong'].queryset = ZHColumn.objects.filter(id=self.instance.belong.id)


class ColumnForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ColumnForm, self).__init__(*args, **kwargs)
        if self.instance.creator:
            self.fields['creator'].queryset = ZHUser.objects.filter(id=self.instance.creator.id)


class ColumnAdmin(admin.ModelAdmin):
    search_fields = ['name', 'slug', 'hash']
    form = ColumnForm


class RandomColumnAdmin(admin.ModelAdmin):
    search_fields = ['slug', 'hash']


class UserAdmin(admin.ModelAdmin):
    search_fields = ['slug', 'hash']


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['title', 'token']
    form = AritcleForm


admin.site.register(Proxy)
admin.site.register(ZHArticle, ArticleAdmin)
admin.site.register(ZHUser, UserAdmin)
admin.site.register(ZHColumn, ColumnAdmin)
admin.site.register(Tag)
admin.site.register(ZHRandomColumn, RandomColumnAdmin)
