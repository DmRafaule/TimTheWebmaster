from MyBlog.settings import MEDIA_URL, ALLOWED_HOSTS
import Post.models as Post_M
from datetime import datetime
import math


def get_how_old_human_in_years(birth_date: str, birth_date_str_frm: str) -> int:
    day_of_birth = datetime.strptime(birth_date, birth_date_str_frm).date()
    today = datetime.today().date()
    me_years = today - day_of_birth
    return math.trunc(me_years.days/365)


def get_latest_post(number: int, category_queryset: Post_M.Category):
    new_posts = list()
    posts = category_queryset.objects.filter(isPublished=True)
    if (len(posts) > number):
        post = posts.latest('timeUpdated')
        for i in range(0, number):
            new_posts.append(post)
            posts = posts.exclude(id=post.id)
            post = posts.latest('timeUpdated')

    return new_posts


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
    selected_special = ("articles", "news", "tools", "services")
    for selected in selected_special:
        categories_result.append(categories.get(slug=selected))
        categories = categories.exclude(slug=selected)
    return getNotEmptyCategories(categories_result)


# Get only those categories that represent content part of my website
def getNotSpecialLowLevelCategories(categories):
    selected_special = ("tools", "services")
    for selected in selected_special:
        categories = categories.exclude(slug=selected)
    return categories


def initDefaults(request):
    categories = Post_M.Category.objects.all()
    categories_special = getSpecialTopLevelCategories(categories)
    # Categories(categories_special) that gonna appear in first level of menu
    # All other (categories) gonna be in second lever under content menu
    domain_name = ALLOWED_HOSTS[0]
    popular_posts = get_latest_post(1, Post_M.Tool)
    popular_posts += get_latest_post(1, Post_M.Article)
    popular_posts += get_latest_post(1, Post_M.News)

    context = {
        'categories_special': categories_special,
        'domain_name': domain_name,
        'popular_posts': popular_posts,
    }
    
    return context
