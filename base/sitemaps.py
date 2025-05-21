from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import *
from base.views import *


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        priorities = {
            'home': 1.0
        }
        return priorities.get(item, 0.5)  # default priority if not found

    def changefreq(self, item):
        changefreqs = {
            'home': 'hourly'
        }
        return changefreqs.get(item, 'monthly')



class VideoSitemap(Sitemap):
    limit = 10000
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Video.objects.all().order_by('-id')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return '/video/' + obj.slug



class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Category.objects.all().order_by('-id')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return '/category/' + obj.slug



class ProfileSitemap(Sitemap):
    changefreq = "weekly"
    limit = 20000
    priority = 0.9

    def items(self):
        return Profile.objects.all().order_by('-id')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return '/onlyfans-model/' + obj.user.username

