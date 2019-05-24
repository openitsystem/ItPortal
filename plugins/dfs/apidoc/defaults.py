# -*- coding: utf-8 -*-

from django.conf import settings

ignore_namespaces = ()

API_DOC_IGNORE_NAMESPACES = getattr(settings, 'API_DOC_IGNORE_NAMESPACES', ignore_namespaces)

api_doc_title = 'Welcome to Django API Document'

API_DOC_TITLE = getattr(settings, 'API_DOC_TITLE', api_doc_title)

API_DOC_API_DOMAIN = getattr(settings, 'API_DOC_API_DOMAIN', '')


skins = {'skin-blue', 'skin-black', 'skin-purple', 'skin-yellow', 'skin-red', 'skin-green'}

skin = getattr(settings, 'API_DOC_SKIN', 'skin-blue')
API_DOC_SKIN = skin if skin in skins else 'skin-blue'
