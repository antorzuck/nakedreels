from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from base.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('video/<str:slug>', video_get),
    path('category/<slug:slug>/', category_view, name='category'),
    path('search/', search_video_view, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
