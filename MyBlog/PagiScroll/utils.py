import Post.models as Post_M
from datetime import datetime
from django.db.models import Q
from itertools import chain


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

def get_posts_by_letters(letters, queryset):
    if len(letters) > 0:
        trms = queryset.none()
        for letter in letters:
            trms = list(chain(trms, queryset.filter(termin__istartswith=letter)))
        return queryset.filter(termin__in=trms)
    else:
        return queryset

def get_posts_by_platforms(platforms, queryset):
    for platform in platforms:
        queryset = queryset.filter(platforms=platform)

    if len(queryset) == 0:
        return []
    else:
        return queryset 