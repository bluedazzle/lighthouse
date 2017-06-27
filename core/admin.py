from django.contrib import admin
from core.models import *


# Register your models here.

class ColumnAdmin(admin.ModelAdmin):
    search_fields = ['name', 'slug', 'hash']


class RandomColumnAdmin(admin.ModelAdmin):
    search_fields = ['slug', 'hash']


class UserAdmin(admin.ModelAdmin):
    search_fields = ['slug', 'hash']


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ['title', 'token']


admin.site.register(Proxy)
admin.site.register(ZHArticle, ArticleAdmin)
admin.site.register(ZHUser, UserAdmin)
admin.site.register(ZHColumn, ColumnAdmin)
admin.site.register(Tag)
admin.site.register(ZHRandomColumn, RandomColumnAdmin)
