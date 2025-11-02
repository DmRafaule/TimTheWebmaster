from datetime import datetime
from itertools import chain
import math
import os

from django.db.models import Q
from django.db.models import Case, When
from django.utils.translation import get_language

from Website.settings import  ALLOWED_HOSTS, MY_INSTALLED_APPS, BASE_DIR
import Post.models as Post_M
from Engagement.models import Interaction
from .models import Website, Contact
from .forms import FeedbackForm
from Engagement.forms import EmailForm

    
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

def calculate_popularity(views, likes, shares, bookmarks, comments, post_date, current_date=None,
                         zero=1, alpha=2, beta=3, gamma=1.5, delta=0.1):
    """
    Calculate the popularity score of a post considering engagement and post age.
    
    Args:
    - views (int): number of post views
    - likes (int): number of likes
    - shares (int): number of shares
    - bookmarks (int): number of bookmarks
    - comments (int): number of comments
    - post_date (datetime): the date when the post was published
    - current_date (datetime, optional): the date to calculate the age from; 
      defaults to now if None
    - alpha, beta, gamma (float): weights for comments, shares, bookmarks respectively
    - delta (float): decay rate for post age influence
    
    Returns:
    - float: popularity score
    """
    if current_date is None:
        current_date = datetime.now().replace(tzinfo=None)
        
    age_days = (current_date - post_date.replace(tzinfo=None)).days
    if age_days < 0:
        age_days = 0  # just in case post_date is in the future
    
    total_weighted_engagements = (zero * likes + alpha * comments + beta * shares + gamma * bookmarks)
    
    if views == 0:
        engagement_rate = 0
    else:
        engagement_rate = total_weighted_engagements / views
    
    # Popularity decays exponentially with age
    popularity_score = engagement_rate * math.exp(-delta * age_days)
    
    return popularity_score

def extract_slug(path):
    parts = [segment for segment in path.split('/') if segment]  # Remove empty parts
    return parts[-1]

def get_posts_by_popularity(number: int, model):
    posts_to_compare = {}
    language_code = get_language()
    for interaction in Interaction.objects.filter(url__startswith=f"/{language_code}/"):
        slug = extract_slug(interaction.url)
        post = model.objects.filter(slug=slug)
        if len(post) > 0:
            date = post.first().timeUpdated
            score = calculate_popularity(
                interaction.views,
                interaction.likes,
                interaction.shares,
                interaction.bookmarks,
                interaction.comments,
                date
            )
            posts_to_compare[slug] = score

    sorted_by_popularity = sorted(posts_to_compare.items(), key=lambda x: x[1], reverse=True)
    top_slugs = [slug for slug, score in sorted_by_popularity[:number]]
    # Вернем QuerySet постов, соответствующих top slugs, в том же порядке среза
    preserved_order = Case(*[When(slug=slug, then=pos) for pos, slug in enumerate(top_slugs)])
    queryset = model.objects.filter(slug__in=top_slugs).order_by(preserved_order)
    return queryset

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

def getSpecialTopLevelCategories(categories):
    ''' Возвращает либо список всех категорий для отображения, либо пустой список '''
    try:
        website_conf = Website.objects.get(is_current=True)
        categories_on_side = website_conf.categories_to_display_on_side_menu.all()
    except:
        categories_on_side = categories

    return categories_on_side

def initDefaults(request):
    ''' Инициализирует общие для всех контекстные переменные '''
    # Пытаемся получить текущие настройки сайта
    try:
        website_conf = Website.objects.get(is_current=True)
        popular_articles_in_footer = website_conf.popular_articles_on_footer.all()
        popular_tools_in_footer = website_conf.popular_tools_on_footer.all()
        image_preview = website_conf.default_image_preview
        contacts_for_orders = website_conf.contacts_for_orders
    except:
        popular_articles_in_footer = []
        popular_tools_in_footer = []
        image_preview = None
        contacts_for_orders = []
    # Получаем категории для отображения в боковом меню
    categories = Post_M.Category.objects.all()
    categories_special = getSpecialTopLevelCategories(categories)
    # Сохраняем доменное имя
    domain_name = ALLOWED_HOSTS[0]
    # Сохраняем популярные посты (статьи + инструменты)
    popular_posts = list(chain(popular_articles_in_footer, popular_tools_in_footer))
    # Обозначаем дефолтное изображени
    default_post_preview = image_preview
    # Получаем все контакты
    contacts = Contact.objects.all()
    if not len(contacts_for_orders.all()) > 0:
        contacts_for_orders = contacts
    # Создаём и отправляем пустую форму по умолчанию, GET-запрос
    form = FeedbackForm()
    # Создаём и отправляем пустую форму по умолчанию, GET-запрос
    email_form = EmailForm()

    context = {
        'categories_special': categories_special,
        'domain_name': domain_name,
        'contacts': contacts,
        'contacts_for_orders': contacts_for_orders,
        'popular_posts': popular_posts,
        'default_post_preview': default_post_preview,
        'feedback_form': form,
        'email_subscription_form': email_form
    }
    return context


def get_apps_root_dirs():
        apps_root_dirs = []
        # Собираю пути до корневых директорий приложений
        for app_conf in MY_INSTALLED_APPS:
            CWD = BASE_DIR
            app_folders = app_conf.split('.')
            for app_folder in app_folders:
                if app_folder == "apps":
                    break
                CWD = os.path.join(CWD, app_folder)
            apps_root_dirs.append(CWD)
        
        return apps_root_dirs