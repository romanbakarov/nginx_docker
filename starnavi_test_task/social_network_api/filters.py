from django_filters import rest_framework as filters

from social_network_api.models import Like


class LikeAnalyticsFilter(filters.FilterSet):
    date_from = filters.DateTimeFilter(field_name='liked_at', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='liked_at', lookup_expr='lte')

    class Meta:
        model = Like
        fields = ('liked_at', 'like')
