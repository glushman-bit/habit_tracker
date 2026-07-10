from rest_framework.pagination import LimitOffsetPagination


class HabitPaginator(LimitOffsetPagination):
    """Пагинация списка привычек."""

    default_limit = 5
    max_limit = 100
    limit_query_param = "limit"
    offset_query_param = "offset"
