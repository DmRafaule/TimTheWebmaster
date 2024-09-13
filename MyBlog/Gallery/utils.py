from Main.models import Image
from Post.models import Article
from .models import Image as GalleryImage
from datetime import datetime, date

def byDate(img):
    return datetime.strptime(img['image'].timeCreated.date().strftime('%m/%d/%Y %I:%M %p'), '%m/%d/%Y %I:%M %p')

def getLatesImagesAll() -> list:
    images = []
    # Get all images marked as ART + related tags
    for img in Image.objects.filter(category=Image.ART):
        images.append({'image': img, 'tags': img.tags.all()})
    # Get all previews in articles + related tags
    for post in Article.objects.exclude(preview=''):
        images.append({'image': Image(file=post.preview,timeCreated=post.timeCreated), 'tags': post.tags.all()})
    # Get all images in gallery and combine them all + related tags
    for img in GalleryImage.objects.all(): 
        images.append({'image': img, 'tags': img.tags.all()})
    images = sorted(images, key=byDate, reverse=True)
    return images