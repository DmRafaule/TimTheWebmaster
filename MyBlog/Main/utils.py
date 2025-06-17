from MyBlog.settings import  ALLOWED_HOSTS
import Post.models as Post_M
from datetime import datetime
from .models import Website, Contact
from django.db.models import Q
import math
from itertools import chain

    
def get_how_old_human_in_years(birth_date: str, birth_date_str_frm: str) -> int:
    ''' Возвращает возраст человека  '''
    day_of_birth = datetime.strptime(birth_date, birth_date_str_frm).date()
    today = datetime.today().date()
    me_years = today - day_of_birth
    # Округляем до целого числа
    return math.trunc(me_years.days/365)

def get_posts_by_tag(tag_name: str, category_queryset: Post_M.Category):
    ''' Возвращает посты в зависимоти от наличия в них искомого тега '''
    tags = Post_M.Tag.objects.filter(Q(name_ru=tag_name) | Q(name_en=tag_name) | Q(slug_ru=tag_name) | Q(slug_en=tag_name))
    posts = category_queryset.objects.filter(isPublished=True, tags__in=tags)
    return posts

def getAllWithTags(queryset, tags, threshold = None):
    ''' Возвращает посты в зависимости от наличия в них искомых тегов '''
    for tag in tags:
        queryset = queryset.filter(tags=tag)

    if len(queryset) == 0:
        return []
    else:
        return queryset 

def get_latest_post(number: int, queryset):
    ''' Возвращает последние посты, в зависимости от того удовлетворяют ли они минимальному необходимому количеству для возврата '''
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
    ''' Возвращает инструмент по указанному адресу'''
    # Делим строку
    urlList = _url.split('/')
    # Чистим не нужный мусор
    c = urlList.count('') 
    for i in range(c): 
        urlList.remove('') 
    # Проверяем есть ли такой инструмент
    slug = urlList[-1]
    tool_qs = Post_M.Tool.objects.filter(slug=slug)
    if len(tool_qs) > 0:
        return tool_qs[0]
    else:
        return None

def getNotEmptyCategories(categories):
    ''' Отфильтровывает все категории, которые не имеют постов '''
    categories_result = []
    for category in categories:
        if Post_M.Post.objects.filter(category=category, isPublished=True):
            categories_result.append(category)
    return categories_result

# Create queryset with special categories
def getSpecialTopLevelCategories(categories):
    try:
        website_conf = Website.objects.get(is_current=True)
        categories_on_side = website_conf.categories_to_display_on_side_menu.all()
    except:
        categories_on_side = []

    return getNotEmptyCategories(categories)

def initDefaults(request):
    try:
        website_conf = Website.objects.get(is_current=True)
        popular_articles_in_footer = website_conf.popular_articles_on_footer.all()
        popular_tools_in_footer = website_conf.popular_tools_on_footer.all()
        image_preview = website_conf.default_image_preview
    except:
        popular_articles_in_footer = []
        popular_tools_in_footer = []
        image_preview = None

    categories = Post_M.Category.objects.all()
    categories_special = getSpecialTopLevelCategories(categories)
    # Categories(categories_special) that gonna appear in first level of menu
    # All other (categories) gonna be in second lever under content menu
    domain_name = ALLOWED_HOSTS[0]
    popular_posts = list(chain(popular_articles_in_footer, popular_tools_in_footer))
    default_post_preview = image_preview
    contacts = Contact.objects.all()
    context = {
        'categories_special': categories_special,
        'domain_name': domain_name,
        'contacts': contacts,
        'popular_posts': popular_posts,
        'default_post_preview': default_post_preview,
    }
    
    return context
