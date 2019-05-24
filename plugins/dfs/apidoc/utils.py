# -*- coding: utf-8 -*-

import re

from django_api_doc import defaults as settings


def resolve_urls(url_patterns, prefix=''):
    """
    resolve url

    example: your urls.py like this

        url(r'^signup/$', views.SignupView.as_view(), name='signup'),
        url(r'^login/$', views.LoginView.as_view(), name='login'),
        url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

        url(r'^accounts/', include('apps.account.urls', namespace='accounts')),

    :return: {
        'login': 'login',
        'signup': 'signup,
        'logout': 'logout',
        'account-user_info': 'user_info',
        'account-like_user': 'like_user',
    }
    """
    data = []
    for url_pattern in url_patterns:
        if hasattr(url_pattern, 'name') and url_pattern.name:
            key = '%s|%s' % (prefix, url_pattern.name) if prefix else url_pattern.name
            data.append({
                'key': key,
                'name': url_pattern.name
            })
        elif hasattr(url_pattern, 'namespace'):
            if url_pattern.namespace in settings.API_DOC_IGNORE_NAMESPACES:
                continue

            key = '%s|%s' % (prefix, url_pattern.namespace) if prefix else url_pattern.namespace
            data.extend(resolve_urls(url_pattern.urlconf_module.urlpatterns, prefix=key))
    return data


def get_url_pattern_by_name(url_patterns, name, prefix=''):
    """
    get url pattern by url name

    :param url_patterns: url_patterns, eg: urlresolvers.get_resolver().url_patterns
    :param name: url namespace + url name, eg: account-login
    :param prefix: the prefix of key
    :return: url_pattern
    """
    for url_pattern in url_patterns:
        if hasattr(url_pattern, 'name') and url_pattern.name:
            key = '%s|%s' % (prefix, url_pattern.name) if prefix else url_pattern.name
            if key == name:
                return url_pattern
        elif hasattr(url_pattern, 'namespace'):
            if url_pattern.namespace in settings.API_DOC_IGNORE_NAMESPACES:
                continue

            key = '%s|%s' % (prefix, url_pattern.namespace) if prefix else url_pattern.namespace
            ret = get_url_pattern_by_name(url_pattern.urlconf_module.urlpatterns, name, prefix=key)
            if ret:
                return ret


def format_url(url):
    if url.startswith('^'):
        url = '/' + url[1:]

    if url.endswith('$'):
        url = url[:-1]

    param_re = re.compile('\(\?P(<.*?>).*?\)')
    url = param_re.sub(r'\1', url)

    if settings.API_DOC_API_DOMAIN:
        url = '%s%s' % (settings.API_DOC_API_DOMAIN.rstrip('/'), url)
    return url
