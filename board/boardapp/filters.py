from django_filters import FilterSet, DateFilter
from .models import Post
 
# создаём фильтр
class PostFilter(FilterSet):
    dateCreation = DateFilter(
        field_name='dateCreation',
        label='Дата поста',
        lookup_expr='gte',
        input_formats=['%d-%m-%Y', '%d-%m','%m', '%d', '%m-%Y', '%d.%m.%Y'],  # Укажите желаемый формат ввода даты
        )
    class Meta:
        model = Post
        fields = {
            'categoryType':['exact'],
		    'title': ['icontains'],
		    'user':['exact'],
        }