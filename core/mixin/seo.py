# coding: utf-8
from __future__ import unicode_literals
from Lighthouse.settings import HOST


class HostMixin(object):
    def get_context_data(self, **kwargs):
        context = super(HostMixin, self).get_context_data(**kwargs)
        context['host'] = HOST
        return context
