from .models import Category
from .utils import get_trending_searches_cached


def trending_searches(request):
    return {
        'trending_searches': get_trending_searches_cached()
    }

def categories_processor(request):
    categories = Category.objects.all()
    return {'categories': categories}
