"""kleosserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin

from splash.views import *
from college.views import *
from users.views import *
from home.views import *
from questions.views import *
from sponser.views import *
from about_us.views import *

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^splash_screen/$', splash_screen),			
    url(r'^welcome/$', welcome_screen),
    url(r'^update_details/$', update_user_details),
    url(r'^sign_up/$', user_sign_up),
    url(r'^verify_otp/$', verify_otp),
    url(r'^resend_otp/$', resend_otp),
    url(r'^login/$', user_login),
    url(r'^forgot_password/$', forgot_password),
    url(r'^tab_list/$', tab_list),  
    url(r'^profile/$', profile),
    url(r'^story/$', story),
    url(r'^question_list/$', question_list),
    url(r'^bonus/$', bonus),
    url(r'^hints/$', hints),
    url(r'^sponsor_list/$', sponsor_list),
    url(r'^about_us/$', about_us),       
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
