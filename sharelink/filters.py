import django_filters
from sharelink.models import ShareLink
from django import forms
from django.db.models import Q
class_attrs='form-control form-control-lg'

class ShareFilter(django_filters.FilterSet):
    search=django_filters.CharFilter(
        method='my_search',
        label='',
        widget=forms.TextInput(attrs={'class':class_attrs})
    )
    class Meta:
        model=ShareLink
        fields=['search']
    def my_search(self,queryset,name,value):
        return queryset.filter(
            Q(title__icontains=value)|Q(link__url__icontains=value)
        )   