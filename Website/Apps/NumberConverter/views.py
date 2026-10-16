import re

from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse

from Main.utils import initDefaults
from Post.models import Article

from base_to_base_number.main import BaseNumber
from base_to_base_number.main import get_base_regex


BASE_MAP = {
    '2': {'short': 'bin', 'name': _('Двоичная')},
    '3': {'short': 'triplex', 'name': _('Троичная')},
    '4': {'short': 'qua', 'name': _('Четверичная')},
    '5': {'short': 'qui', 'name': _('Пятеричная')},
    '6': {'short': 'sen', 'name': _('Шестеричная')},
    '7': {'short': 'sep', 'name': _('Семеричная')},
    '8': {'short': 'oct', 'name': _('Восьмеричная')},
    '9': {'short': 'non', 'name': _('Девятеричная')},
    '10': {'short': 'dec', 'name': _('Десятичная')},
    '11': {'short': 'und', 'name': _('Одиннадцатеричная')},
    '12': {'short': 'duo', 'name': _('Двенадцатеричная')},
    '13': {'short': 'terdec', 'name': _('Тринадцатеричная')},
    '14': {'short': 'tet', 'name': _('Четырнадцатеричная')},
    '15': {'short': 'pen', 'name': _('Пятнадцатеричная')},
    '16': {'short': 'hex', 'name': _('Шестнадцатеричная')},
    '17': {'short': 'hep', 'name': _('Семнадцатеричная')},
    '18': {'short': 'octdec', 'name': _('Восемнадцатеричная')},
    '19': {'short': 'ennea', 'name': _('Девятнадцатеричная')},
    '20': {'short': 'vig', 'name': _('Двадцатеричная')},
    '21': {'short': 'unvig', 'name': _('Двадцатиодноричная')},
    '22': {'short': 'duovig', 'name': _('Двадцатидвухричная')},
    '23': {'short': 'trivig', 'name': _('Двадцатитрехричная')},
    '24': {'short': 'tetravig', 'name': _('Двадцатичетырехричная')},
    '25': {'short': 'pentavig', 'name': _('Двадцатипятиричная')},
    '26': {'short': 'hexavig', 'name': _('Двадцатишестеричная')},
    '27': {'short': 'septemvig', 'name': _('Двадцатисемеричная')},
    '28': {'short': 'octovig', 'name': _('Двадцативосьмеричная')},
    '29': {'short': 'enneavig', 'name': _('Двадцатидевятеричная')},
    '30': {'short': 'tri', 'name': _('Тридцатеричная')},
    '31': {'short': 'untri', 'name': _('Тридцатиодноричная')},
    '32': {'short': 'duotri', 'name': _('Тридцатидвухричная')},
    '33': {'short': 'tritri', 'name': _('Тридцатитрехричная')},
    '34': {'short': 'tetratri', 'name': _('Тридцатичетырехричная')},
    '35': {'short': 'pentatri', 'name': _('Тридцатипятиричная')},
    '36': {'short': 'hexatri', 'name': _('Тридцатишестиричная')},
}

# Lookup map from short code back to base number
REVERSE_BASE_MAP = {data['short']: k for k, data in BASE_MAP.items()}


def convert_number(query_number: str, from_base_code: int, to_base_code: int):
    str_number = None
    regx = get_base_regex(from_base_code) # TODO: Проверка на отправку не кода но строчки 
    # It is a number
    if re.match(regx, query_number):
        base_number = BaseNumber(query_number, from_base_code)
        fraction = base_number.get_fraction_raw()
        precision = 2
        if fraction:
            precision = len(fraction)
        str_number = base_number.convert_to(int(to_base_code), precision)
    return str_number


def tool_main(request, from_base=None, to_base=None):
    context = initDefaults(request)
    is_home_page = False
    # Posts to insert into page
    first_post = Article.objects.filter(slug="why-to-build-number-base-convertor").first()
    second_post = Article.objects.filter(slug="how-to-convert-number-from-one-base-to-another").first()
    main_posts = []
    if first_post:
        main_posts.append(first_post)
    if second_post:
        main_posts.append(second_post)


    # 1. Handle POST request from the main page form
    if request.method == 'POST':
        from_val = request.POST.get('from', '10')
        to_val = request.POST.get('to', '16')
        query_val = request.POST.get('query', '')

        # Convert numeric base string to 3-letter code (default to original if unmapped)
        from_str = BASE_MAP[from_val]['short'] if from_val in BASE_MAP else from_val
        to_str = BASE_MAP[to_val]['short'] if to_val in BASE_MAP else to_val

        redirect_url = reverse('number-converter-specified', kwargs={"from_base": from_str, "to_base": to_str})

        # Append query parameter if present
        if query_val:
            redirect_url = f"{redirect_url}?query={query_val}"

        # If submitted via HTMX, tell HTMX to redirect the browser to the new URL
        if request.headers.get('HX-Request'):
            response = HttpResponse(status=200)
            response['HX-Redirect'] = redirect_url
            return response

        # Fallback for standard non-HTMX POST form submission
        return redirect(redirect_url)

    # 2. Handle GET request after redirect (or direct access)
    from_code = REVERSE_BASE_MAP.get(from_base, '10')
    to_code = REVERSE_BASE_MAP.get(to_base, '16')
    query_text = request.GET.get('query', '')
    result_type = request.GET.get('type', None)

    result_str = ""
    if query_text:
        query_numbers = str(query_text).split()
        str_numbers = []
        # Check if it is muliple numbers
        if len(query_numbers) > 1:
            for query_number in query_numbers:
                query_number = query_number.strip()
                str_number = convert_number(query_number, int(from_code), int(to_code))
                if str_number:
                    str_numbers.append(str_number)
                else:
                    pass

            result_str = " ".join(str_numbers)
            result_numbers = str_numbers

        # Otherwise, single number
        else:
            query_number = query_numbers[0].strip()
            result_str = convert_number(query_number, int(from_code), int(to_code))
            result_numbers = [result_str]
            

    if not from_base:
        from_base = 'dec'
        is_home_page = True
        
    if not to_base:
        to_base = 'hex'
        is_home_page = True

    context.update({
        'from_code': from_code,
        'to_code': to_code,
        'from_base': from_base,
        'to_base': to_base,
        'from_name': BASE_MAP.get(from_code, {}).get('name', _('Десятичная')),
        'to_name': BASE_MAP.get(to_code, {}).get('name', _('Шестнадцатеричная')),
        'query_text': query_text,
        'is_home_page': is_home_page,
        'main_posts': main_posts,
        'result': result_str,
    })

    match result_type:
        case 'json':
            return JsonResponse({
                "from_base": from_code,
                "to_base": to_code,
                "numbers": result_numbers
            })
        case 'raw':
            return HttpResponse(result_str)
    
    return TemplateResponse(request, 'NumberConverter/index.html', context=context)