from itertools import chain

from django.db import models
from django.utils import timezone


class Shader(models.Model):
    name = models.CharField(max_length=256, unique=True)
    shader_id = models.CharField(max_length=64, unique=True)
    user_id = models.CharField(max_length=100, null=True)
    is_for_library = models.BooleanField(default=False)
    fragment_src = models.TextField(blank=False)
    vertex_src = models.TextField(blank=False)
    default_geometry_data_indx = models.IntegerField(default=0)
    render_mode = models.CharField(max_length=64, default="TRIANGLES")
    bg = models.CharField(max_length=64)
    buffers = models.TextField(blank=False, default='')
    sizes = models.TextField(blank=False, default='')

    def __str__(self):
        return self.shader_id
