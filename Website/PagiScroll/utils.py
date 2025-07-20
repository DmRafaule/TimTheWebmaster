from itertools import chain

from datetime import datetime
from django.db.models import Q

import Post.models as Post_M


def get_this_day_posts(queryset: Post_M.Post):
    ''' Получает посты, которые были написанны сегодня '''
    today = datetime.today().date()
    return queryset.filter(timeCreated__date=today)

def get_this_week_posts(queryset):
    ''' Получает посты, которые были написанны на этой неделе '''
    this_year = datetime.today().date().year
    week_number = datetime.today().date().isocalendar().week
    return queryset.filter(Q(timeCreated__week=week_number) & Q(timeCreated__year=this_year))

def get_this_month_posts(queryset):
    ''' Получает посты, которые были написанны в этом месяце '''
    this_year = datetime.today().date().year
    this_month = datetime.today().date().month
    return queryset.filter(Q(timeCreated__month=this_month) & Q(timeCreated__year=this_year))

def get_this_year_posts(queryset):
    ''' Получает посты, которые были написанны в этом году '''
    this_year = datetime.today().date().year
    return queryset.filter(timeCreated__year=this_year)

def get_posts_by_week_days(days: list[int], queryset: Post_M.Post):
    ''' Получает посты, по указанным дням недели 
    
    Параметры:
        - **days**: дни недели от 1 до 7, где 1 - понедельник 7 - воскресенье
        - **queryset**: группа запросов
    '''
    if len(days) > 0:
        return queryset.filter(timeCreated__iso_week_day__in=days)
    else:
        return queryset

def get_posts_by_month_days(days: list[int], queryset):
    ''' Получает посты, по указанным дням месяца от 1 до 31 '''
    if len(days) > 0:
        return queryset.filter(timeCreated__day__in=days)
    else:
        return queryset

def get_posts_by_months(months: list[int], queryset):
    ''' Получает посты, по указанным месяцам от 1 до 12 '''
    if len(months) > 0:
        return queryset.filter(timeCreated__month__in=months)
    else:
        return queryset

def get_posts_by_years(years: list[int], queryset):
    ''' Получает посты, по указанным годам '''
    if len(years) > 0:
        return queryset.filter(timeCreated__year__in=years)
    else:
        return queryset

def get_posts_by_letters(letters: str, queryset):
    # Неактуальна
    if len(letters) > 0:
        trms = queryset.none()
        for letter in letters:
            trms = list(chain(trms, queryset.filter(termin__istartswith=letter)))
        return queryset.filter(termin__in=trms)
    else:
        return queryset

def get_posts_by_platforms(platforms, queryset):
    ''' Получает инструменты по наличию того или иного объекта Platform в ней '''
    for platform in platforms:
        queryset = queryset.filter(platforms=platform)

    if len(queryset) == 0:
        return []
    else:
        return queryset 

def calculate_pages(total_items: int, items_per_page: int) -> int:
    ''' Вычисляет количество страниц необходимых для пагинации определённого к-ва элементов '''
    if total_items <= 0 or items_per_page <= 0:
        return 1
    
    return -(-total_items // items_per_page)

def in_order(queryset, is_recent):
    ''' Сортирует набор запросов по времени создания '''
    if is_recent == 'true':
        order = '-timeCreated'
    else:
        order = 'timeCreated'

    return queryset.order_by(order)

def in_alphabetic(queryset, is_alphabetic):
    # Не актуальна
    if is_alphabetic != 'ignored':
        if is_alphabetic == 'true':
            order = '-termin'
        else:
            order = 'termin'
        # Resort posts by alphabet
        return queryset.order_by(order)
    else:
        return queryset