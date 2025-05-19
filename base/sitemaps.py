from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import *
from base.views import *
class StaticViewSitemap(Sitemap):
    def items(self):
        return [home]

    def location(self, item):
        return reverse(item)


class VideoSitemap(Sitemap):
    limit = 1
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Video.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
    def location(self, obj):
        return '/video/' + obj.slug

class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

