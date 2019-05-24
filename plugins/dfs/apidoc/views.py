# -*- coding: utf-8 -*-

import sys
import re
import inspect
import markdown

from django.utils.encoding import smart_str

from django.views.generic import View
from django.shortcuts import render
from django.core import urlresolvers
from django.core.urlresolvers import RegexURLPattern, reverse

from django_api_doc.utils import resolve_urls, get_url_pattern_by_name, format_url
from django_api_doc import defaults as settings

if sys.version_info < (3, 0):
    from urllib import unquote
else:
    from urllib.parse import unquote


class APIDocView(View):
    template_name = 'django_api_doc/docs.html'

    def get_doc_content(self, url_name):
        url_patterns = urlresolvers.get_resolver().url_patterns
        url_pattern = get_url_pattern_by_name(url_patterns, url_name)
        if not isinstance(url_pattern, RegexURLPattern):
            return {}

        view = url_pattern.callback.view_class
        items = []
        for method in view.http_method_names:
            if method == 'options' or not hasattr(view, method):
                continue

            # difference of py2 and py3
            if sys.version_info < (3, 0):
                doc_content = smart_str(inspect.getdoc(getattr(view, method))).decode('utf-8')
            else:
                doc_content = smart_str(inspect.getdoc(getattr(view, method)))

            if doc_content:
                doc_content = markdown.markdown(doc_content, ['tables', 'attr_list'], safe_mode='escape')
            items.append({
                'method': method.upper(),
                'content': doc_content,
            })

        try:
            url = reverse(url_name.replace('|', ':'))
        except Exception as e:
            ret = re.findall('(?:pattern\(s\) tried: \[)(.+)(?:\])', e.__str__())
            if ret:
                url = ret[0]
            else:
                url = url_pattern.regex.pattern

        return {
            'title': view.__doc__ if view.__doc__ else view.__name__,
            'url': format_url(url),
            'items': items,
        }

    def get(self, request, url_name=None):
        doc_base_url = unquote(request.get_full_path()).replace(url_name, '')
        data = {
            'url_namespaces': [],
            'url_names': [],
            'doc_title': settings.API_DOC_TITLE,
            'doc_base_url': doc_base_url,
            'skin': settings.API_DOC_SKIN,
        }

        # get all name and namespace by url conf
        url_patterns = urlresolvers.get_resolver().url_patterns
        for url_pattern in url_patterns:
            if hasattr(url_pattern, 'name') and url_pattern.name:
                data['url_names'].append({
                    'key': url_pattern.name,
                    'name': url_pattern.name
                })
            elif hasattr(url_pattern, 'namespace') and url_pattern.namespace:
                # if namespace in ignore namespaces setting
                if url_pattern.namespace in settings.API_DOC_IGNORE_NAMESPACES:
                    continue

                # if namespace is api_doc's namespace
                space_url = url_pattern.regex.pattern.replace('^', '/')
                if space_url == doc_base_url:
                    continue

                url_names = resolve_urls(
                    url_pattern.urlconf_module.urlpatterns,
                    prefix=url_pattern.namespace,
                )
                data['url_namespaces'].append({
                    'name': url_pattern.namespace,
                    'url_names': url_names
                })

        data['doc'] = self.get_doc_content(url_name)
        return render(request, self.template_name, data)
