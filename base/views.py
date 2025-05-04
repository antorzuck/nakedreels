from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from .models import Video, Comment, Category, Profile, Tag
from django.views.decorators.csrf import csrf_exempt


def home(request):
    recent_videos = Video.objects.all().order_by('-created_at')[:15]
    for_you_videos = Video.objects.order_by('?')[:15]
    featured_profiles = Profile.objects.annotate(video_count=Count('videos')).order_by('-video_count')[:5]
    trending_categories = Category.objects.annotate(video_count=Count('video')).order_by('-video_count')[:6]

    context = {
        'recent_videos': recent_videos,
        'for_you_videos': for_you_videos,
        'featured_profiles': featured_profiles,
        'trending_categories': trending_categories,
    }
    return render(request, 'home.html', context)





def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    videos = Video.objects.filter(category=category).order_by('-created_at')[:20]

    return render(request, 'category.html', {
        'category': category,
        'videos': videos
    })


def search_video_view(request):
    query = request.GET.get('q', '')
    videos = Video.objects.none()

    if query:
        videos = Video.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    return render(request, 'search_results.html', {
        'query': query,
        'videos': videos
    })



@csrf_exempt 
def post_comment_view(request, video_slug):
    if request.method == 'POST':
        video = get_object_or_404(Video, slug=video_slug)
        text = request.POST.get('text', '').strip()
        if text and request.user.is_authenticated:
            Comment.objects.create(
                video=video,
                profile=request.user.profile,
                text=text
            )
        return HttpResponseRedirect(reverse('video_detail', args=[video_slug]))


def video_get(request, slug):
    video = get_object_or_404(Video, slug=slug)
    comments = video.comments.select_related('profile__user').order_by('-created_at')
    up_next_videos = Video.objects.exclude(id=video.id).order_by('?')[:10]

    context = {
        'video': video,
        'comments': comments,
        'up_next_videos': up_next_videos,
    }
    return render(request, 'video.html', context)


def v(r):
    return render(r, 'video.html')