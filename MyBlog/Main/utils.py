from MyBlog.settings import MEDIA_URL, ALLOWED_HOSTS
import Post.models as Post_M
from datetime import datetime
from .models import Website
from django.db.models import Q
import math
from itertools import chain
from bs4 import BeautifulSoup

    
def page_to_string(html):
    soup = BeautifulSoup(html, features='lxml')
    text_blocks = ''
    for el in soup.find_all('div', class_='text'):
        text_blocks += el.getText()
    return text_blocks

def get_how_old_human_in_years(birth_date: str, birth_date_str_frm: str) -> int:
    day_of_birth = datetime.strptime(birth_date, birth_date_str_frm).date()
    today = datetime.today().date()
    me_years = today - day_of_birth
    return math.trunc(me_years.days/365)


def get_posts_by_tag(tag_name: str, category_queryset: Post_M.Category):
    tags = Post_M.Tag.objects.filter(Q(name_ru=tag_name) | Q(name_en=tag_name) | Q(slug_ru=tag_name) | Q(slug_en=tag_name))
    posts = category_queryset.objects.filter(isPublished=True, tags__in=tags)
    return posts

def get_this_day_posts(queryset: Post_M.Post):
    today = datetime.today().date()
    return queryset.filter(timeCreated__date=today)

def get_this_week_posts(queryset):
    this_year = datetime.today().date().year
    week_number = datetime.today().date().isocalendar().week
    return queryset.filter(Q(timeCreated__week=week_number) & Q(timeCreated__year=this_year))

def get_this_month_posts(queryset):
    this_year = datetime.today().date().year
    this_month = datetime.today().date().month
    return queryset.filter(Q(timeCreated__month=this_month) & Q(timeCreated__year=this_year))

def get_this_year_posts(queryset):
    this_year = datetime.today().date().year
    return queryset.filter(timeCreated__year=this_year)

def get_posts_by_week_days(days, queryset):
    if len(days) > 0:
        return queryset.filter(timeCreated__iso_week_day__in=days)
    else:
        return queryset

def get_posts_by_month_days(days, queryset):
    if len(days) > 0:
        return queryset.filter(timeCreated__day__in=days)
    else:
        return queryset

def get_posts_by_months(months, queryset):
    if len(months) > 0:
        return queryset.filter(timeCreated__month__in=months)
    else:
        return queryset

def get_posts_by_years(years, queryset):
    if len(years) > 0:
        return queryset.filter(timeCreated__year__in=years)
    else:
        return queryset


def get_latest_post(number: int, queryset):
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
    website_conf = Website.objects.get(is_current=True)
    categories_result = website_conf.categories_to_display_on_side_menu.all()
    categories = categories.exclude(slug__in=categories_result)
    return getNotEmptyCategories(categories_result)

def toDebugFile(msg, isFirst = False):
    if isFirst:
        with open('my_debug.txt', 'w', encoding='utf-8') as file:
            file.write('DEBUG FILE v 0.2\n\n')    

    with open('my_debug.txt', 'a+', encoding='utf-8') as file:
        file.write(msg+'\n')


def initDefaults(request):
    website_conf = Website.objects.get(is_current=True)
    categories = Post_M.Category.objects.all()
    categories_special = getSpecialTopLevelCategories(categories)
    # Categories(categories_special) that gonna appear in first level of menu
    # All other (categories) gonna be in second lever under content menu
    domain_name = ALLOWED_HOSTS[0]
    popular_posts = list(chain(website_conf.popular_articles_on_footer.all(), website_conf.popular_tools_on_footer.all()))

    context = {
        'categories_special': categories_special,
        'domain_name': domain_name,
        'popular_posts': popular_posts,
    }
    
    return context
