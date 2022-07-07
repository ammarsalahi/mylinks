import django_filters
from listlink.models import ListLink
from django.db.models import Q
from django import forms
class_attrs='form-control form-control-lg'

class ListFilter(django_filters.FilterSet):
    search=django_filters.CharFilter(
        method='my_search',
        label='',
        widget=forms.TextInput(attrs={'class':class_attrs})
    )
    class Meta:
        model=ListLink
        fields=['search']
    def my_search(self,queryset,name,value):
         return queryset.filter(
             Q(title__icontains=value)|Q(addlink__url__icontains=value)
         )   