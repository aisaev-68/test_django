from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Lesson, LessonView


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name',)


class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = ('status', 'viewing_time')


class LessonSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    view_info = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('name', 'product_name', 'view_info')

    def get_product_name(self, lesson):
        return [{'name': product.name} for product in lesson.products.all()]

    def get_view_info(self, lesson):
        return [{'status': view.viewed, 'viewing_time': view.viewing_time} for view in lesson.lesson_view.all()]


class LessonByProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор уроков по продуктам.
    name - название урока.
    product_id - id продукта.
    product_name - имя продукта.
    view_info - {
        'status' -состояние,
        'last_view_date' - последняя дата просмотра
        }
    """
    product_name = serializers.SerializerMethodField()
    view_info = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('name', 'product_name', 'view_info')

    def get_product_name(self, lesson):
        return [{'name': product.name} for product in lesson.products.all()]

    def get_view_info(self, lesson):
        return [{'status': view.viewed, 'last_view_date': lesson.last_view_date} for view in lesson.lesson_view.all()]


class ProductStatsSerializer(serializers.Serializer):
    """
    product_id - id продукта.
    product_name - поле представляет имя продукта.
    total_lessons - общее количество уроков для данного продукта.
    total_view_duration - общая продолжительность просмотра для данного продукта.
    total_students - общее количество учеников, занимающихся на данном продукте.
    access_count - общее количество доступов к данному продукту.
    average_view_duration_per_lesson - среднюю продолжительность просмотра урока на данном продукте.
    acquisition_rate - процент приобретения продукта.
    """
    product_id = serializers.IntegerField(source='id')
    product_name = serializers.CharField(source='name')
    total_lessons = serializers.IntegerField()
    total_view_duration = serializers.IntegerField()
    total_students = serializers.IntegerField()
    access_count = serializers.IntegerField()
    average_view_duration_per_lesson = serializers.SerializerMethodField()
    acquisition_rate = serializers.SerializerMethodField()

    def get_average_view_duration_per_lesson(self, obj):
        if obj['total_lessons'] > 0:
            return obj['total_view_duration'] / obj['total_lessons']
        return 0

    def get_acquisition_rate(self, obj):
        total_users = User.objects.count()  # Общее количество пользователей
        if total_users > 0:
            return (obj['access_count'] / total_users) * 100
        return 0
