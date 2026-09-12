from Post.models import Post
from django.db.models import Q

def getSlugFromURL(url: str) -> str:
    url_elements_clean = []
    for el in url.split('/'):
        if len(el) > 0:
            url_elements_clean.append(el)
    return url_elements_clean[2]

def get_root_comments(comments, root_comments:list = [], not_root_comments:list = []):
    for comment in comments:
        if len(comment.replies.all()) > 0:
            not_root_comments.append(comment)
        else:
            root_comments.append(comment)
    
    for comment in root_comments:
        if comment in not_root_comments:
            not_root_comments.append(comment)
            root_comments.remove(comment)
    
    for comment in not_root_comments:
        if comment in root_comments:
            not_root_comments.append(comment)
            root_comments.remove(comment)
        else:
            not_root_comments.remove(comment)
            root_comments.append(comment)

def convert_old_urls(url: str) -> str:
    parts = [p for p in url.split('/') if p]
    # Старый URL состоит из 3 сегментов: ['en', 'articles', 'article-1']
    if len(parts) == 3:
        code, category, slug = parts[0], parts[1], parts[2]
        post = Post.objects.filter(slug=slug).first()
        if post and post.subcategory:
            field_name = f"slug_{code}"
            sub_slug = getattr(post.subcategory, field_name, post.subcategory.slug)
            return f"/{code}/{category}/{sub_slug}/{slug}/"
    return url