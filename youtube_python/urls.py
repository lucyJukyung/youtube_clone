"""youtube_python URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from youtube.views import HomeView, NewVideo, LoginView, RegisterView, VideoView, CommentView, VideoFileView, LogoutView, MyVideoView, Trending
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view()),
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('new_video', NewVideo.as_view()),
    path('video/<int:id>', VideoView.as_view()),
    path('comment', CommentView.as_view()),
    path('get_video/<file_name>', VideoFileView.as_view()),
    path('logout', LogoutView.as_view()),
    path('my_videos', MyVideoView.as_view()),
    path('trending', Trending.as_view()),
]

urlpatterns += staticfiles_urlpatterns()

from django.conf import settings
from django.conf.urls import include, url  # For django versions before 2.0
from django.urls import include, path  # For django versions from 2.0 and up

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
          path('__debug__/', include(debug_toolbar.urls)),

          # For django versions before 2.0:
          # url(r'^__debug__/', include(debug_toolbar.urls)),

      ] + urlpatterns
