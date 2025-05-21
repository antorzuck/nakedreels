from django.utils import timezone
from django.core.cache import cache
from django.db.models import Count
from datetime import timedelta
from .models import SearchQuery

def get_trending_searches_cached(hours=24, limit=6, cache_key='trending_searches', timeout=300):
   
    trending = cache.get(cache_key)
    if trending is not None:
        return trending

   
    time_threshold = timezone.now() - timedelta(hours=hours)
    trending = (
        SearchQuery.objects.filter(searched_at__gte=time_threshold)
        .values('query')
        .annotate(search_count=Count('id'))
        .order_by('-search_count')[:limit]
    )

   
    cache.set(cache_key, list(trending), timeout)
    return trending
