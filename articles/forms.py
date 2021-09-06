from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, ImageField, HiddenInput
from django import forms

from .models import Article
from stocksetfsbonds.models import StockETFBond

from dal import autocomplete
from taggit.models import Tag


# class ArticleForm(ModelForm):
class ArticleForm(autocomplete.FutureModelForm):
    # stocks_etfs_or_bonds = ModelMultipleChoiceField(queryset=StockETFBond.objects.all(),
    #                                                 widget=CheckboxSelectMultiple, required=False)
    title_image = ImageField(required=False)

    class Meta:
        model = Article
        fields = ('title', 'slug', 'author', 'title_image', 'description', 'body', 'tags', 'stocks_etfs_or_bonds')
        widgets = {'author': HiddenInput,
                   'tags': autocomplete.TaggitSelect2('articles:tag-autocomplete'),
                   'stocks_etfs_or_bonds': autocomplete.ModelSelect2Multiple(url='articles:security-autocomplete')}