from MyBlog.settings import MEDIA_URL, ALLOWED_HOSTS
import Post.models as Post_M
from datetime import datetime
import math


def get_how_old_human_in_years(birth_date: str, birth_date_str_frm: str) -> int:
    day_of_birth = datetime.strptime(birth_date, birth_date_str_frm).date()
    today = datetime.today().date()
    me_years = today - day_of_birth
    return math.trunc(me_years.days/365)


def get_posts_by_tag(tag_name: str, category_queryset: Post_M.Category):
    tags = Post_M.Tag.objects.filter(name=tag_name)
    posts = category_queryset.objects.filter(isPublished=True, tags__in=tags)
    return posts

def get_latest_post(number: int, queryset: Post_M.Article):
    new_posts = list()
    posts = queryset.filter(isPublished=True)
    if (len(posts) > number):
        post = posts.latest('timeCreated')
        for i in range(0, number):
            new_posts.append(post)
            posts = posts.exclude(id=post.id)
            post = posts.latest('timeCreated')

    return new_posts

def get_most_popular_post() -> Post_M.Article: 
    articles = Post_M.Article.objects.filter(isPublished=True)
    scores = []
    for article in articles:
        like_mod = article.likes * 2
        shares_mode = article.shares * 10
        views = article.viewed
        interaction_score = like_mod + shares_mode + 0.0000001
        scores.append({
            'score': views/interaction_score,
            'article': article,
        })
    # Will sort them descending
    return min(scores, key=lambda x:x['score'])['article']

    

# Filtering out all empty categories
def getNotEmptyCategories(categories):
    categories_result = []
    for category in categories:
        if Post_M.Post.objects.filter(category=category, isPublished=True):
            categories_result.append(category)
    return categories_result


# Create queryset with special categories
def getSpecialTopLevelCategories(categories):
    categories_result = []
    selected_special = ("articles", "tools")
    for selected in selected_special:
        categories_result.append(categories.get(slug=selected))
        categories = categories.exclude(slug=selected)
    return getNotEmptyCategories(categories_result)


# Get only those categories that represent content part of my website
def getNotSpecialLowLevelCategories(categories):
    selected_special = ("tools" )
    for selected in selected_special:
        categories = categories.exclude(slug=selected)
    return categories


def initDefaults(request):
    categories = Post_M.Category.objects.all()
    categories_special = getSpecialTopLevelCategories(categories)
    # Categories(categories_special) that gonna appear in first level of menu
    # All other (categories) gonna be in second lever under content menu
    domain_name = ALLOWED_HOSTS[0]
    internal_tools = Post_M.Tool.objects.filter(type=Post_M.Tool.INTERNAL)
    popular_posts = get_latest_post(2, internal_tools)
    popular_posts.append(get_most_popular_post())

    context = {
        'categories_special': categories_special,
        'domain_name': domain_name,
        'popular_posts': popular_posts,
    }
    
    return context
