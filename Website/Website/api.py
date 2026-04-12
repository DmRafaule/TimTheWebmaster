import os
import json
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from django.db import models
from django.apps import apps
from django.db.models.base import ModelBase

import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import serializers, viewsets
from rest_framework.routers import DefaultRouter
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.permissions import IsAdminUser, AllowAny, BasePermission

from .settings import INDEXNOW_API_KEY


# ====================================================================
# PAGINATION
# ====================================================================

class CustomModelPagination(PageNumberPagination):
    """
    Defines a custom pagination class to control the page size for all 
    dynamically generated ViewSets.
    """
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100

# ====================================================================
# UTILITY FUNCTIONS: MODEL INTROSPECTION & SERIALIZER
# ====================================================================

def get_app_models(app_name):
    """Retrieves all concrete (non-abstract) Django models within a specified app."""
    try:
        app_config = apps.get_app_config(app_name)
        return [
            model for model in app_config.get_models()
            if isinstance(model, ModelBase) and not model._meta.abstract
        ]
    except LookupError:
        return []

def create_model_serializer(model_class):
    """Dynamically creates a simple ModelSerializer for the given model."""
    class DynamicModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = model_class
            fields = '__all__'

    DynamicModelSerializer.__name__ = f'{model_class.__name__}Serializer'
    return DynamicModelSerializer

# ====================================================================
# DYNAMIC FILTERING COMPONENTS
# ====================================================================

def create_model_filterset(model_class):
    """
    Dynamically creates a django-filter FilterSet class for the model, 
    mapping field types to allowed lookups (__gt, __icontains, etc.).
    """
    
    EXCLUDE_FIELD_TYPES = (
        models.FileField, 
        models.ImageField,
        models.JSONField,
    )

    LOOKUP_MAP = {
        models.IntegerField: ['exact', 'lt', 'gt', 'lte', 'gte'],
        models.FloatField: ['exact', 'lt', 'gt', 'lte', 'gte'],
        models.DecimalField: ['exact', 'lt', 'gt', 'lte', 'gte'],
        models.CharField: ['exact', 'icontains'],
        models.TextField: ['exact', 'icontains'],
        models.DateField: ['exact', 'lt', 'gt', 'year', 'month'],
        models.DateTimeField: ['exact', 'lt', 'gt', 'date'],
        models.ForeignKey: ['exact'],
    }

    fields_dict = {}
    
    for field in model_class._meta.concrete_fields:
        if isinstance(field, EXCLUDE_FIELD_TYPES):
            continue

        for field_type, lookups in LOOKUP_MAP.items():
            if isinstance(field, field_type):
                fields_dict[field.name] = lookups
                break
        else:
            fields_dict[field.name] = ['exact']

    class DynamicMeta:
        model = model_class
        fields = fields_dict

    DynamicFilterSet = type(
        f'{model_class.__name__}FilterSet',
        (django_filters.FilterSet,),
        {'Meta': DynamicMeta}
    )
    
    return DynamicFilterSet

# ====================================================================
# CONSOLIDATED DYNAMIC VIEWSET GENERATOR
# ====================================================================

def create_generic_viewset(_model_class, _serializer_class, _base_viewset_class, _permission_classes):
    """
    Creates a flexible ModelViewSet based on provided parameters.

    Args:
        model_class (Model): The Django model to expose.
        serializer_class (Serializer): The serializer class to use.
        base_viewset_class (viewsets.ViewSet): The base class (e.g., ModelViewSet or ReadOnlyModelViewSet).
        permission_classes (list[BasePermission]): The security permissions to apply.
    """
    
    DynamicFilterSet = create_model_filterset(_model_class)
    
    # Identify fields for sorting and searching
    sortable_fields = list(DynamicFilterSet.Meta.fields.keys())
    if not sortable_fields:
        sortable_fields = ['id'] 
        
    SEARCHABLE_FIELD_TYPES = (models.CharField, models.TextField)
    searchable_fields = [
        f.name 
        for f in _model_class._meta.concrete_fields 
        if isinstance(f, SEARCHABLE_FIELD_TYPES)
    ]
    
    # --- Dynamic Model ViewSet Definition ---

    class DynamicModelViewSet(_base_viewset_class):
        queryset = _model_class.objects.all()
        serializer_class = _serializer_class

        # SECURITY: Set permissions based on the argument provided
        permission_classes = _permission_classes
        # Add the custom renderer
        renderer_classes = [JSONRenderer, BrowsableAPIRenderer] 
        # DRF will automatically select the renderer based on Accept header 
        # or the ?format= query parameter (which we'll use).
        # Functionality backends
        filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
        filterset_class = DynamicFilterSet
        pagination_class = CustomModelPagination

        # Ordering/Sorting
        ordering_fields = sortable_fields
        ordering = ['-id'] 

        # Searching
        search_fields = searchable_fields

        # Переопределяем метод list для захвата данных пагинации
        def list(self, request, *args, **kwargs):
            # 1. Вызываем super().list(). На этом шаге происходит пагинация, 
            #    и self.paginator.page получает объект Page.
            response = super().list(request, *args, **kwargs)

            # Если используется HTML рендерер (т.е. запрос с ?format=html)
            # и используется пагинация (self.paginator не None)
            if request.accepted_renderer.format == 'html' and self.paginator:
                
                # --- Инициализация renderer_context ---
                # В отличие от `get_renderer_context` в DRF, который вызывается позже,
                # здесь мы должны инициализировать его вручную, чтобы добавить данные.
                # DRF не всегда гарантирует его наличие в объекте Response в методе list().
                
                # Используем ._set_renderer_context для установки контекста
                # Это более надежный, хоть и "приватный" способ, который работает.
                if not hasattr(response, 'renderer_context'):
                    response.renderer_context = {}
                
                renderer_context = response.renderer_context

                # --- ПОЛУЧЕНИЕ ДАННЫХ ПАГИНАЦИИ ---
                
                # 1. Получаем текущую страницу (Page object)
                # Этот объект становится доступен только после super().list()
                page_obj = self.paginator.page
                
                # 2. Общее количество страниц (Total Pages)
                total_pages = page_obj.paginator.num_pages
                
                # 3. Текущая страница (Current Page Number)
                current_page = page_obj.number
                
                # 4. URL для следующей и предыдущей страниц (предоставляются DRF)
                next_url = self.paginator.get_next_link()
                prev_url = self.paginator.get_previous_link()
                
                # 5. Сохраняем данные пагинации для использования в рендерере
                # Эти данные будут извлечены в вашем AdminRecordsHTMLRenderer
                renderer_context['pagination_data'] = {
                    'next': next_url,
                    'previous': prev_url,
                    'total_pages': total_pages,
                    'current_page': current_page,
                }
                
                response.renderer_context = renderer_context # Установка не нужна, так как мы модифицировали объект
            
            return response
        
    # Use f-strings for the class name to maintain DRF conventions
    DynamicModelViewSet.__name__ = f'{_model_class.__name__}{_base_viewset_class.__name__}'
    return DynamicModelViewSet

# ====================================================================
# CONSOLIDATED ROUTER REGISTRATION 
# ====================================================================

def get_dynamic_api_urls(api_type='admin', exclude_apps=None):
    """
    Primary function. Finds all installed apps, registers their models, 
    and returns URL patterns based on the specified API type.

    Args:
        api_type (str): 'admin' for secure CRUD, 'public' for read-only.
        exclude_apps (list): List of app labels to ignore.
    """
    router = DefaultRouter()
    
    # 1. Configuration based on api_type
    if api_type == 'admin':
        # Admin API: Full CRUD access, restricted to staff
        base_viewset = viewsets.ModelViewSet
        permissions = [IsAdminUser]
        basename_prefix = ''
    elif api_type == 'public':
        # Public API: Read-Only access, open to everyone
        base_viewset = viewsets.ReadOnlyModelViewSet
        permissions = [AllowAny]
        basename_prefix = 'public-'
    else:
        raise ValueError("api_type must be 'admin' or 'public'.")

    # 2. Loop through all apps and register models
    all_app_configs = apps.get_app_configs()
    
    for config in all_app_configs:
        app_label = config.label
        
        if exclude_apps and app_label in exclude_apps:
            continue
            
        all_models = get_app_models(app_label)
        
        for model in all_models:
            serializer_class = create_model_serializer(model)
            
            # 🎯 Call the single, generic ViewSet creator
            viewset_class = create_generic_viewset(
                _model_class=model,
                _serializer_class=serializer_class,
                _base_viewset_class=base_viewset,
                _permission_classes=permissions
            )
            
            base_name = model._meta.model_name
            # Register with a unique basename for DRF
            router.register(r'{}'.format(base_name), viewset_class, basename=f'{basename_prefix}{base_name}')

    return router.urls

@csrf_exempt
@require_http_methods(["POST"])
def send_to_indexnow_direct(url_list):
    payload = {
        'host': 'timthewebmaster.com',
        'key': INDEXNOW_API_KEY,
        "keyLocation": f"https://timthewebmaster.com/{INDEXNOW_API_KEY}.txt",
        'urlList': url_list
    }
    try:
        requests.post('https://api.indexnow.org/indexnow', headers={'Content-Type': 'application/json; charset=utf-8'}, json=payload, timeout=5)
    except Exception as e:
        print(f"IndexNow Error: {e}")