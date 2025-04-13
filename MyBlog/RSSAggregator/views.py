from django.shortcuts import render
from django.http import JsonResponse
from django.template.response import TemplateResponse
from Main.utils import initDefaults
from .models import Feed
import feedparser
import ssl

def tool_main(request):
    context = initDefaults(request)
    return TemplateResponse(request, 'RSSAggregator/rss-aggregator.html', context=context)

def loadFeeds(request):
    user_id = request.session.session_key
    feeds = Feed.objects.filter(user_id=user_id)
    context = {
            'feeds': feeds,
    }
    return render(request, 'RSSAggregator/rss-feed-group.html', context=context)

def submitFeed(request):
    if request.method == 'POST':
        
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context

        feed = feedparser.parse(request.POST['feedname'])
        # Hack if empty string with '' will be sended
        if not len(request.POST['feedname']) >= 1:
            return JsonResponse({'common': "Error: Too short URL"}, status=500)
        # Check if feed is real
        if not feed['bozo'] or len(feed['entries']) > 0:
            pass
        else:
            return JsonResponse({'common': f"Error: {feed['bozo_exception']}"}, status=500)
        
        # Check if feed is already in database
        if Feed.objects.filter(source=request.POST['feedname'], user_id=request.session.session_key).exists():
            return JsonResponse({'common': "Error: This feed already in database."}, status=500)

        feed = Feed(
            user_id=request.session.session_key,
            source=request.POST['feedname'],
            group=None,
        )
        feed.save()
        context = {
            'feeds': [feed],
        }

    return render(request, 'RSSAggregator/rss-feed-group.html', context=context)

def deleteFeed(request):
    status=500
    if request.method == 'POST':
        user_id = request.session.session_key
        feed = Feed.objects.filter(user_id=user_id, id=request.POST['id'])
        if feed.exists():
            status=200
            feed.delete()
    
    return JsonResponse({},status=status)

def sort_by_date(element):
    return element.published

def getFeedPosts(request):
    if request.method == 'GET':
        user_id = request.session.session_key
        num_to_return = int(request.GET['size'])
        offset = int(request.GET['offset'])
        feed_id = request.GET['id']
        feed = Feed.objects.get(user_id=user_id, id=feed_id)
        
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        feed_items = feedparser.parse(feed.source)['entries']

        
        is_sorted = request.GET.get('sorted', 'false')
        if is_sorted == 'true':
            feed_items.sort(key=sort_by_date)
        # Add model field to hold parsed data
        
        posts = []
        for item in feed_items[offset:offset + num_to_return]:
            posts.append({
                'title' : item.title,
                'date_published': item.published,
                'description': item.description,
                'link': item.link,

            })
        context = {
            'posts': posts,
            'feed_length': len(feed_items),
            'feed_offset': offset,
            'feed_id': feed_id,
            'feed_sorted': is_sorted,
        }
    
    return render(request, 'RSSAggregator/rss-feed-post.html', context=context)