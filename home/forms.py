from django.forms import ModelForm
from django.forms.widgets import TextInput
from home.models import Search, NewsSearch


class SearchForm(ModelForm):
    class Meta:
        model = Search
        fields = ('search_text', 'num_tweets',)
        widgets = {
            'search_text': TextInput(attrs={'class': 'search-box-full',
                                            'placeholder': 'Search for brand/product/service keywords (e.g.,) #something (or) @someone',
                                            'pattern': '#.+|@.+'}),
            'num_tweets': TextInput(attrs={'class': 'search-box-full', 'value': '150', 'type': 'number', 'min': '1'}),
        }


class NewsSearchForm(ModelForm):
    class Meta:
        model = NewsSearch
        fields = ('search_text', 'num_articles',)
        widgets = {
            'search_text': TextInput(attrs={'class': 'search-box-full',
                                            'placeholder': 'Search for brand/product/service keywords (e.g.,) amazon (or) walmart'
                                            }),  # 'pattern': '#.+|@.+'
            'num_articles': TextInput(attrs={'class': 'search-box-full', 'value': '100', 'type': 'number', 'min': '1'}),
        }
