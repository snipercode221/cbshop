#!/usr/local/bin/python
# -*- coding: utf-8 -*-


"""cbsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, handler404, handler500
from django.contrib import admin
from shop import views
from django.conf.urls.static import static
from django.conf import settings

handler404 = views.handler404
handler500 = views.handler500


urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', views.accueil, name="accueil"),
                  url(r'^shop/', include('shop.urls')),
                  url(r'^(?P<nom>[\w\-]+)/$', views.redirection, name="boutique"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
