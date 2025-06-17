from MyBlog.settings import  ALLOWED_HOSTS
import Post.models as Post_M
from datetime import datetime
from .models import Website, Contact
from django.db.models import Q
import math
from itertools import chain

    
def get_how_old_human_in_years(birth_date: str, birth_date_str_frm: str) -> int:
    day_of_birth = datetime.strptime(birth_date, birth_date_str_frm).date()
    today = datetime.today().date()
    me_years = today - day_of_birth
    return math.trunc(me_years.days/365)

def get_posts_by_tag(tag_name: str, category_queryset: Post_M.Category):
    tags = Post_M.Tag.objects.filter(Q(name_ru=tag_name) | Q(name_en=tag_name) | Q(slug_ru=tag_name) | Q(slug_en=tag_name))
    posts = category_queryset.objects.filter(isPublished=True, tags__in=tags)
    return posts

# Return only those elements which has all tags in them
def getAllWithTags(queryset, tags, threshold = None):
    for tag in tags:
        queryset = queryset.filter(tags=tag)

    if len(queryset) == 0:
        return []
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

def get_tool(_url):
    urlList = _url.split('/')
    # Clean up after slplit function
    c = urlList.count('') 
    for i in range(c): 
        urlList.remove('') 
    slug = urlList[-1]
    tool_qs = Post_M.Tool.objects.filter(slug=slug)
    if len(tool_qs) > 0:
        return tool_qs[0]
    else:
        return None

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

def initDefaults(request):
    website_conf = Website.objects.get(is_current=True)
    categories = Post_M.Category.objects.all()
    categories_special = getSpecialTopLevelCategories(categories)
    # Categories(categories_special) that gonna appear in first level of menu
    # All other (categories) gonna be in second lever under content menu
    domain_name = ALLOWED_HOSTS[0]
    popular_posts = list(chain(website_conf.popular_articles_on_footer.all(), website_conf.popular_tools_on_footer.all()))
    default_post_preview = website_conf.default_image_preview
    contacts = Contact.objects.all()
    context = {
        'categories_special': categories_special,
        'domain_name': domain_name,
        'contacts': contacts,
        'popular_posts': popular_posts,
        'default_post_preview': default_post_preview,
    }
    
    return context
