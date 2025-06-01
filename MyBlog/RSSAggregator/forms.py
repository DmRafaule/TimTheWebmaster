from django import forms
from django.utils.translation import gettext_lazy as _

import string
import random

from .models import FeedId

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class FeedAddFormEmpty(forms.Form):
    template_name = "RSSAggregator/feed_add.html"
    user_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(widget=forms.HiddenInput(), required=False)
    feed = forms.URLField(label="",required=True, widget=forms.URLInput(attrs={'placeholder': 'https://website-example.com/feed/url/', 'class': "w-full", 'some': ""}))
    feed_id = ''

    def __init__(self, *args, **kwargs):
        self.feed_id = id_generator()
        user_id = kwargs.pop('user_id', None)
        feed = kwargs.pop('feed', None)
        super().__init__(*args, **kwargs)
        self.fields['feed'].widget.attrs['some'] = f'feed-{self.feed_id}'
        if user_id:
            self.initial['user_id'] = user_id
        if feed:
            self.initial['feed'] = feed 

class FeedAddFormWithName(forms.Form):
    template_name = "RSSAggregator/feed_edit.html"
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    feed = forms.URLField(label="", required=True, widget=forms.URLInput(attrs={'placeholder': 'https://website-example.com/feed/url/', 'class': "w-full flex-auto"}))
    name = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'placeholder': 'Your custom name for this feed', 'class': "w-full"}))
    feed_id = ''

    def __init__(self, *args, **kwargs):
        self.feed_id = id_generator()
        feed = kwargs.pop('feed', None)
        name = kwargs.pop('name', None)
        id = kwargs.pop('id', None)
        super().__init__(*args, **kwargs)
        self.fields['feed'].widget.attrs['some'] = f'feed-{self.feed_id}'
        if feed:
            self.initial['feed'] = feed 
        if name:
            self.initial['name'] = name 
        if id:
            self.initial['id'] = id 

class FeedIdForm(forms.ModelForm):
    class Meta:
        model = FeedId
        fields = "__all__"
        exclude = ['similar_user_id']
        widgets = {
            "user_id": forms.TextInput(attrs={"disabled": True}),
        }

    previos_user_id = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': _("Твой предыдущий ID. Скопируй его сюда что бы связать с текущим"), 'class': "w-full"}))