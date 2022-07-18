from django.contrib import admin
from django.urls import path, include, re_path

from .views import index, sample
from about import views as aboutViews

urlpatterns = [
    re_path('^$', index),
    re_path('^sample/$', sample),
    re_path('^admin/', admin.site.urls),
    re_path('^predict/', include('predict.urls')),
    re_path('^about/', include('about.urls')),
]
