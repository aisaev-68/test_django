from django.db.models import Sum, Count, Max
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from product.serializers import (
    LessonSerializer,
    LessonByProductSerializer,
    ProductStatsSerializer,
)
from product.models import Product, Lesson


class LessonListView(APIView):
    """
    Представление для выборки списка всех уроков по всем
    продуктам к которым пользователь имеет доступ, с
    выведением информации о статусе и времени просмотра.
    """

    serializer_class = LessonSerializer

    @swagger_auto_schema(
        operation_description='get lesson items',
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                description='ID user',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def get(self, request, *args, **kwargs) -> Response:

        user_id = self.request.query_params.get('user_id')
        lessons = Lesson.objects.prefetch_related('lesson_view').filter(products__access__user=user_id)
        print(lessons)
        serializer = self.serializer_class(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonByProductView(APIView):
    """
    Представление для выборки уроков по конкретному продукту к
    которому пользователь имеет доступ, с выведением информации
    о статусе и времени просмотра, а также датой последнего
    просмотра ролика.
    """

    serializer_class = LessonByProductSerializer

    @swagger_auto_schema(
        operation_description='get lesson by product items',
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                description='ID user',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'product_id',
                openapi.IN_QUERY,
                description='ID product',
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def get(self, request, *args, **kwargs) -> Response:

        user_id = self.request.query_params.get('user_id')
        product_id = self.request.query_params.get('product_id')
        lessons = Lesson.objects.prefetch_related('lesson_view').filter(
            products__access__product=product_id,
            products__access__user=user_id
        ).annotate(
            last_view_date=Max('lesson_view__viewing_time')
        ).order_by('-last_view_date')

        serializer = self.serializer_class(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductStatsView(APIView):
    """
    Представление для выборки статистики по продуктам:
        1.Количество просмотренных уроков от всех учеников.
        2.Сколько в сумме все ученики потратили времени на просмотр роликов.
        3.Количество учеников занимающихся на продукте.
        4.Процент приобретения продукта (рассчитывается исходя из количества
        полученных доступов к продукту деленное на общее количество пользователей
        на платформе).
    """
    serializer_class = ProductStatsSerializer

    def get(self, request, *args, **kwargs) -> Response:
        product_stats = Product.objects.annotate(
            total_lessons=Count('lessons'),
            total_view_duration=Sum('lessons__view_duration'),
            total_students=Count('access__user', distinct=True),
            access_count=Count('access')
        ).values('id', 'name', 'total_lessons', 'total_view_duration', 'total_students', 'access_count')
        serializer = self.serializer_class(product_stats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
