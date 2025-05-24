from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import os
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.paginator import Paginator
import random
import string




@csrf_exempt
def check_or_create_profile(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    import json
    try:
        data = json.loads(request.body)
        username = data.get('username')
    except:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not username:
        return JsonResponse({'error': 'Username is required'}, status=400)

    user, created = User.objects.get_or_create(username=username)
    Profile.objects.get_or_create(user=user)

    return JsonResponse({'message': 'Profile created or exists'}, status=200)

@csrf_exempt
def upload_video(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    username = request.POST.get('username')
    title = request.POST.get('title')
    desc = request.POST.get('desc', '')
    video_file = request.FILES.get('video')
    thumbnail_file = request.FILES.get('thumbnail')

    if not all([username, title, video_file]):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)

    slug = slugify(title)
    original_slug = slug
    count = 1
    while Video.objects.filter(slug=slug).exists():
        slug = f"{original_slug}-{count}"
        count += 1

    video = Video.objects.create(
        profile=profile,
        title=title,
        slug=slug,
        description=desc,
        video_file=video_file,
        thumbnail=thumbnail_file
    )

    return JsonResponse({'message': 'Video uploaded', 'video_id': video.id}, status=201)



def home(request):
   
    all_recent_videos = Video.objects.all().order_by('-created_at')
    paginator = Paginator(all_recent_videos, 2)  
    page_number = request.GET.get('page')
    recent_videos = paginator.get_page(page_number)

    for_you_videos = Video.objects.order_by('?')[:15]
    featured_profiles = Profile.objects.annotate(video_count=Count('videos')).order_by('-video_count')[:6]
    trending_categories = Category.objects.annotate(video_count=Count('video')).order_by('-video_count')[:6]

    context = {
        'recent_videos': recent_videos,
        'for_you_videos': for_you_videos,
        'featured_profiles': featured_profiles,
        'trending_categories': trending_categories,
    }
    return render(request, 'home.html', context)



def user_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    videos_list = profile.videos.all().order_by('-created_at')  # Assuming BaseModel has created_at

    paginator = Paginator(videos_list, 6)  # Show 6 videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    followed_profiles = request.session.get('followed_profiles', [])
    has_followed = str(video.profile.id) in followed_profiles


    return render(request, 'profile.html', {
        'profile': profile,
        'page_obj': page_obj,
        'has_followed': has_followed,
    })


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
        SearchQuery.objects.create(query=query)
        videos = Video.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
        profiles = Profile.objects.filter(user__username__icontains=query)


    return render(request, 'search.html', {
        'query': query,
        'videos': videos,
        'profiles' : profiles
    })



def generate_random_name():
    return 'User-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@csrf_exempt 
def post_comment_view(request, video_slug):
    if request.method == 'POST':
        video = get_object_or_404(Video, slug=video_slug)
        text = request.POST.get('text', '').strip()

        # Get or set random name in session
        name = request.session.get('commenter_name')
        if not name:
            name = generate_random_name()
            request.session['commenter_name'] = name

        if text and request.user.is_authenticated:
            comment = Comment.objects.create(
                video=video,
                name=name,
                text=text
            )
            return JsonResponse({
                'status': 'success',
                'name': comment.name,
                'text': comment.text,
                'created_at': 'just now'
            })
        return JsonResponse({'status': 'failed'}, status=400)

def video_get(request, slug):
    video = get_object_or_404(Video, slug=slug)
    comments = video.comments.all().order_by('-created_at')
    up_next_videos = Video.objects.exclude(id=video.id).order_by('?')[:10]
    video.views += 1
    video.save()
    liked_videos = request.session.get('liked_videos', [])
    followed_profiles = request.session.get('followed_profiles', [])
    has_followed = str(video.profile.id) in followed_profiles

    context = {
        'video': video,
        'comments': comments,
        'up_next_videos': up_next_videos,
        'liked_videos': liked_videos,
        'has_followed': has_followed,
    }
    return render(request, 'video.html', context)





def videos_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    videos = Video.objects.filter(category=category)

    context = {
        'category': category,
        'videos': videos,
    }

    return render(request, 'category.html', context)



def p(r):
    return render(r, 'category.html')



def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow:",
        "Sitemap: https://nakedreels.com/sitemap.xml",
        "Sitemap: https://nakedreels.com/sitemap-static.xml",
        "Sitemap: https://nakedreels.com/sitemap-video.xml",
        "Sitemap: https://nakedreels.com/sitemap-category.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def like_video(request, video_id):
    liked_videos = request.session.get('liked_videos', [])

    if video_id in liked_videos:
        # Unlike
        liked_videos.remove(video_id)
        video = Video.objects.get(id=video_id)
        video.likes -= 1
        video.save()
        liked = False
    else:
        # Like
        liked_videos.append(video_id)
        video = Video.objects.get(id=video_id)
        video.likes += 1
        video.save()
        liked = True

    request.session['liked_videos'] = liked_videos

    return JsonResponse({
        'liked': liked,
        'likes_count': video.likes,
        'message': "Unliked" if not liked else "Liked"
    })

def follow_user(request, user_id):
    followed_profiles = request.session.get('followed_profiles', [])
    profile_id_str = str(user_id)

    profile = get_object_or_404(Profile, id=user_id)

    if profile_id_str in followed_profiles:
        # Unfollow
        followed_profiles.remove(profile_id_str)
        profile.follow_count = max(profile.follow_count - 1, 0)
        followed = False
    else:
        # Follow
        followed_profiles.append(profile_id_str)
        profile.follow_count += 1
        followed = True

    profile.save()
    request.session['followed_profiles'] = followed_profiles
    request.session.modified = True

    return JsonResponse({
        'followed': followed,
        'follower_count': profile.follow_count,
        'message': "Unfollowed" if not followed else "Followed"
    })
