import os
import re
import shutil
from django.core.management.commands.startapp import Command as BaseCommand
from django.core.management.base import CommandParser


HTML_TEMPLATE_CONTENT = """{% extends 'Post/base_tool.html' %}
{% load static %}
{% load i18n %}

{% block hat_tool %}
{% endblock %}

{% block content_tool %}
{% endblock %}

{% block footer_tool %}
{% endblock %}

{% block scripts_tool %}
    <script src="{% static 'APP_NAME/js/index.min.js' %}"></script>
{% endblock %}

{% block styles_tool %}
    <link type="text/css" rel="stylesheet" href="{% static 'APP_NAME/css/index.min.css' %}"/>
{% endblock %}
"""

VIEWS_TEMPLATE = """from django.shortcuts import render
from django.template.response import TemplateResponse

from Main.utils import initDefaults


def tool_main(request):
    context = initDefaults(request)
    
    return TemplateResponse(request, 'APP_NAME/index.html', context=context)
"""

URLS_TEMPLATE = """from django.urls import path
from .views import tool_main 


urlpatterns = [
    path('URL_SLUG/', tool_main, name='URL_SLUG'),
]
"""

APPS_TEMPLATE = """from django.apps import AppConfig


class APP_NAMEConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'APPS_FOLDER.APP_NAME'
"""


def camel_to_kebab(name: str) -> str:
    """Converts CamelCase or PascalCase app names to kebab-case slug (e.g., NumberConverter -> number-converter)."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


class Command(BaseCommand):
    help = 'Улучшенная версия создания приложений, которая позволяет создавать приложения и сразу их подключать'

    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        app_name = options['name']
        apps_folder_name = 'Apps'

        # Command directory where configuration templates are stored
        command_dir = os.path.dirname(os.path.abspath(__file__))

        # Target directory inside Apps/ folder
        target = options.get('directory')
        if target is None:
            apps_dir = os.path.join(os.getcwd(), apps_folder_name)
            os.makedirs(apps_dir, exist_ok=True)
            app_dir = os.path.join(apps_dir, app_name)
            options['directory'] = app_dir
        else:
            app_dir = os.path.abspath(target)

        # Let Django generate default app files inside Apps/AppName
        super().handle(*args, **options)

        url_slug = camel_to_kebab(app_name)

        # 1. Update apps.py
        apps_py_content = (
            APPS_TEMPLATE
            .replace('APPS_FOLDER', apps_folder_name)
            .replace('APP_NAME', app_name)
        )
        with open(os.path.join(app_dir, 'apps.py'), 'w', encoding='utf-8') as f:
            f.write(apps_py_content)

        # 2. Setup Static folders & files (-S flag)
        os.makedirs(os.path.join(app_dir, 'locale', app_name), exist_ok=True)
        static_dir = os.path.join(app_dir, 'static', app_name)
        img_dir = os.path.join(static_dir, 'img')
        js_dir = os.path.join(static_dir, 'js')
        css_dir = os.path.join(static_dir, 'css')

        for directory in [img_dir, js_dir, css_dir]:
            os.makedirs(directory, exist_ok=True)

        open(os.path.join(js_dir, 'index.js'), 'a').close()
        open(os.path.join(css_dir, 'index.css'), 'a').close()

        # 3. Setup Template folders & index.html (-T flag)
        templates_dir = os.path.join(app_dir, 'templates', app_name)
        os.makedirs(templates_dir, exist_ok=True)

        content = HTML_TEMPLATE_CONTENT.replace('APP_NAME', app_name)
        with open(os.path.join(templates_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(content)

        # 4. Setup views.py and urls.py (-U flag)
        views_content = VIEWS_TEMPLATE.replace('APP_NAME', app_name)
        with open(os.path.join(app_dir, 'views.py'), 'w', encoding='utf-8') as f:
            f.write(views_content)

        urls_content = URLS_TEMPLATE.replace('URL_SLUG', url_slug)
        with open(os.path.join(app_dir, 'urls.py'), 'w', encoding='utf-8') as f:
            f.write(urls_content)

        # 5. Copy and process NPM configuration files from command folder
        npm_files = [
            'babel.config.json',
            'package.json',
            'postcss.config.js',
            'tailwind.config.js',
            'webpack.config.js'
        ]

        for filename in npm_files:
            source_file = os.path.join(command_dir, filename)
            dest_file = os.path.join(app_dir, filename)

            if os.path.exists(source_file):
                with open(source_file, 'r', encoding='utf-8') as sf:
                    file_content = sf.read()

                # Replace 'NumberConverter' references with the new app name
                file_content = file_content.replace('NumberConverter', app_name)

                with open(dest_file, 'w', encoding='utf-8') as df:
                    df.write(file_content)

        # 6. Register App in Website/settings.py
        settings_path = os.path.join(os.getcwd(), 'Website', 'settings.py')
        if os.path.exists(settings_path):
            with open(settings_path, 'r', encoding='utf-8') as sf:
                settings_code = sf.read()

            app_config_class = f"{app_name}Config"
            app_setting_line = f"    '{apps_folder_name}.{app_name}.apps.{app_config_class}',"

            if app_setting_line not in settings_code:
                # Find the end of MY_INSTALLED_APPS list and insert new app
                my_apps_match = re.search(r'MY_INSTALLED_APPS\s*=\s*\[(.*?)\]', settings_code, re.DOTALL)
                if my_apps_match:
                    list_content = my_apps_match.group(1).rstrip()
                    # Add comma to last item if missing
                    if list_content and not list_content.strip().endswith(','):
                        list_content += ','
                    updated_list = f"MY_INSTALLED_APPS = [{list_content}\n{app_setting_line}\n]"
                    settings_code = settings_code[:my_apps_match.start()] + updated_list + settings_code[my_apps_match.end():]

                    with open(settings_path, 'w', encoding='utf-8') as sf:
                        sf.write(settings_code)

        # 7. Register App route in Website/urls.py after the last 'tools/' entry line
        website_urls_path = os.path.join(os.getcwd(), 'Website', 'urls.py')
        if os.path.exists(website_urls_path):
            with open(website_urls_path, 'r', encoding='utf-8') as uf:
                lines = uf.readlines()

            url_line = f"    path('tools/', include('{apps_folder_name}.{app_name}.urls')),\n"

            # Prevent duplicate registration
            if not any(url_line.strip() in line for line in lines):
                last_tools_index = -1

                # Locate the index of the last line containing path('tools/', ...)
                for idx, line in enumerate(lines):
                    if "path('tools/'," in line or 'path("tools/",' in line:
                        last_tools_index = idx

                if last_tools_index != -1:
                    lines.insert(last_tools_index + 1, url_line)
                else:
                    # Fallback if no tools/ entry is present
                    for idx, line in enumerate(lines):
                        if line.strip().startswith('urlpatterns += i18n_patterns('):
                            lines.insert(idx + 1, url_line)
                            break

                with open(website_urls_path, 'w', encoding='utf-8') as uf:
                    uf.writelines(lines)