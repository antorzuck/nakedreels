
from django.contrib import admin
from django.urls import path
from base.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('video', v),
    path('category/<slug:slug>/', category_view, name='category'),
    path('search/', search_video_view, name='search'),
]
