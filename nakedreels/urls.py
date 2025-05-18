from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from base.views import *
from django.contrib.sitemaps.views import sitemap, index
from base.sitemaps import StaticViewSitemap, VideoSitemap, CategorySitemap



sitemaps = {
    'video': VideoSitemap,
    'category': CategorySitemap,
    'static': StaticViewSitemap,
}



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('video/<str:slug>', video_get, name='video_detail'),
    path('category/<slug:slug>/', category_view, name='category'),
    path('search/', search_video_view, name='search'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
    path('api/check_or_create_profile/', check_or_create_profile, name='check_or_create_profile'),
    path('api/upload_video/', upload_video, name='upload_video'),
    path('category/<slug:category_slug>/', videos_by_category, name='videos_by_category'),

    path("sitemap.xml/", index, {'sitemaps': sitemaps}, name='sitemap-index'),
    path("sitemap-<section>.xml", sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),


  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
