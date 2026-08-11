from django.contrib import admin
from Apps.ShaderToy.models import Shader


class ShaderAdmin(admin.ModelAdmin):
    list_display = (
            'name',
            'shader_id',
            'user_id',
            'render_mode',
    )
    list_display_links = ('name',)
    search_fields = ('name',)


admin.site.register(Shader, ShaderAdmin)
