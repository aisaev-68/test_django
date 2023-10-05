from django.contrib import admin
from product.models import Product, Lesson, LessonView, Access


class LessonInline(admin.TabularInline):
    model = Lesson.products.through  # Используем модель промежуточной таблицы
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'href')
    list_filter = ('name',)
    search_fields = ('name',)
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'href', 'view_duration')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(LessonView)
class LessonViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'lesson', 'viewing_time', 'viewed')
    list_filter = ('lesson', 'viewed')
    search_fields = ('lesson',)


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    list_filter = ('user', 'product')
    search_fields = ('product',)
