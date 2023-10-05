import datetime

from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from django.contrib.auth.models import User


class Product(models.Model):
    """
    Модель продуктов.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_products',
                              verbose_name='Владелец продукта')
    name = models.CharField(
        max_length=100,
        help_text="Введите название продукта",
        verbose_name="Название продукта")
    href = models.CharField(
        max_length=100,
        help_text="Введите ссылку на продукт",
        verbose_name="Ссылка на продукт")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'



class Lesson(models.Model):
    """
    Модель уроков.
    """

    name = models.CharField(
        max_length=100,
        help_text="Введите название урока",
        verbose_name="Название урока")
    href = models.CharField(
        max_length=100,
        help_text="Введите ссылку на урок",
        verbose_name="Ссылка на урок")

    view_duration = models.PositiveIntegerField(verbose_name="Продолжительность просмотра (секунды)")
    products = models.ManyToManyField(Product, related_name='lessons', verbose_name='Продукты', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class LessonView(models.Model):
    """
    Модель просмотра уроков.
    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_view', verbose_name="Урок")
    user: User = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    viewing_time = models.DateTimeField(verbose_name="Время просмотра", null=True)
    viewed = models.CharField(max_length=100, verbose_name="Статус просмотра")

    def __str__(self):
        return f"View of {self.lesson.name} by {self.user.username}"

    class Meta:
        verbose_name = 'Просмотр уроков'
        verbose_name_plural = 'Просмотры уроков'




class Access(models.Model):
    """
    Модель доступа к продуктам.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access',
                             verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='access',
                                verbose_name='Продукт')

    def __str__(self):
        return f"Access of {self.user} to {self.product}"

    class Meta:
        verbose_name = 'Доступ к продуктам'
        verbose_name_plural = 'Доступы к продуктам'


@receiver(post_save, sender=Product)
def create_lesson_views_on_connect(sender, instance, created, **kwargs):
    if created:
        for lesson in instance.lessons.all():
            for user in instance.access_users.all():
                LessonView.objects.create(
                    user=user,
                    lesson=lesson,
                    viewing_time=None,
                    viewed='Не просмотрено'
                )
