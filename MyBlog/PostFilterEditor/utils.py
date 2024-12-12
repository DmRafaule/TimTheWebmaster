import re
from .models import PostFilter


def GetCustomFilterPage(url: str) -> bool:
    filter_pages = PostFilter.objects.all()
    values = filter_pages.values('regex_slug','id')
    for value in values:
        slug = value['regex_slug']
        id = value['id']
        if re.match(f'{slug}', url) is not None:
            return PostFilter.objects.get(id=id)
    return None
