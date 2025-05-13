from django import forms
from django.utils.translation import gettext_lazy as _

class TextThiefForm(forms.Form):
    template_name = "TextThief/text-thief-form.html"
    WAYS_TO_CRAWL = {'single-url': _("Один УРЛ"), 'list-url': _("Список УРЛов"), 'whole-website': _("Целый сайт"),}
    WAYS_TO_SAVE  = {'text': _("Весь текст"), 'words': _("Все слова, списком"), 'unique_words': _("Все уникальные слова"), 'tags': _("Теги (Слова с количеством употребления в тексте")}
    urls = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={'placeholder': 'https://website-example.com/some-page/', 'class': "w-full"}))
    selector = forms.CharField(label="", required=False, initial='body', widget=forms.TextInput(attrs={'placeholder': 'any.css>selector', 'class': "w-full"}))
    ways_to_crawl = forms.ChoiceField(label=_("Способ обхода"),widget=forms.RadioSelect(attrs={'class': 'custom-choise-link-thief flex flex-row gap-[10px]'}), choices=WAYS_TO_CRAWL)
    ways_to_save = forms.MultipleChoiceField(initial='text', label=_("Как сохранить результат"), required=False, widget=forms.CheckboxSelectMultiple, choices=WAYS_TO_SAVE)