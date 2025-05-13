from django.db import models
from MyBlog.settings import MEDIA_URL


def file_path(instance, filename):
    # type, which folder to use / projects / articles / news / portfolios
    # slug, which one of the above project/ article / new or portfolio
    return "{0}/{1}/{2}/{3}".format('tools', 'text-thief', 'results', filename)

class TextThiefRecord(models.Model):
    file = models.FileField(upload_to=file_path)

    def get_path(self):
        return "{0}{1}".format(MEDIA_URL, self.file)