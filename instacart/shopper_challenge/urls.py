"""instacart URL Configuration

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
from django.conf.urls import url, include

from django.conf.urls import url, handler404, handler403, handler400, handler500
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = 'shopper_challenge'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^application_success_page/$', views.signup_success, name='success_page'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^update/$', views.update, name='update'),
    url(r'^check_status/$', views.check_status, name='login'),
    url(r'^bulk_upload/(?P<count>(\d+))/$', views.bulk_upload, name='bulk_upload'),
    url(r'^funnel.json/$', views.funnel, name='funnel')
]

urlpatterns += staticfiles_urlpatterns()

handler404 = views.errorpage
handler403 = views.errorpage
handler400 = views.errorpage
handler405 = views.errorpage