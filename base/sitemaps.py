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
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Video.objects.all()

    def lastmod(self, obj):
        return obj.updated_at  # Replace with your actual datetime field


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.updated_at  # Replace with your actual datetime field
