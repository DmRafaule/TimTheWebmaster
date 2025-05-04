from django import forms
from django.utils.translation import gettext_lazy as _

class LinkThiefForm(forms.Form):
    template_name = "LinkThief/link-thief-form.html"
    WAYS_TO_CRAWL = {'single-url': _("Один УРЛ"), 'list-url': _("Список УРЛов"), 'whole-website': _("Целый сайт"),}
    WAYS_TO_SAVE  = {'all': _("Все ссылки"), 'internal': _("Только внутренние ссылки"), 'external': _("Только внешние ссылки"), 'anchor-only': _("Только ссылки с анкорами"), 'anchor-without': _("Только ссылки без анкоров"), 'crawlable': _("Только те, которые можно пройти"), 'crawlable-no': _("Только те, которые не поддаются обходу"), }
    urls = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={'placeholder': 'https://website-example.com/some-page/', 'class': "w-full"}))
    show_table_on_page = forms.BooleanField(label=_("Показать таблицу на этой странице"), required=False, widget=forms.CheckboxInput(attrs={'class': 'custom-choise-link-thief flex flex-row gap-[10px]', 'checked': 'true'}))
    ways_to_crawl = forms.ChoiceField(label=_("Способ обхода"),widget=forms.RadioSelect(attrs={'class': 'custom-choise-link-thief flex flex-row gap-[10px]'}), choices=WAYS_TO_CRAWL)
    ways_to_save = forms.ChoiceField(label=_("Как сохранить результат"), widget=forms.RadioSelect(attrs={'class': ''}), choices=WAYS_TO_SAVE)