from django.urls import path
from .views import LessonListView, LessonByProductView, ProductStatsView

urlpatterns = [
    path('api/lessons/', LessonListView.as_view(), name='lesson-list'),
    path('api/lessons/by_product/', LessonByProductView.as_view(), name='lesson-by-product'),
    path('api/product_stats/', ProductStatsView.as_view(), name='product-stats'),
]