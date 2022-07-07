import django_filters
from publiclink.models import PublicLink
from django import forms
from django.db.models import Q
class_attrs='form-control'

class PublicFilter(django_filters.FilterSet):
    search=django_filters.CharFilter(
        method='my_search',
        label='',
        widget=forms.TextInput(attrs={'class':class_attrs})
    )
    class Meta:
        model=PublicLink
        fields=['search']
    def my_search(self,queryset,name,value):
        return queryset.filter(
            Q(title__icontains=value)|Q(link__url__icontains=value)
        )    