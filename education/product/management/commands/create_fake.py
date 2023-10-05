import random
from django.core.management.base import BaseCommand
from faker import Faker
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from product.models import Product, Lesson, LessonView, Access

fake = Faker()

class Command(BaseCommand):
    help = 'Создание фейковых данных'

    def handle(self, *args, **kwargs):


        num_lesson_views = 10
        num_access = 7
        num_products = [f'Product_{i + 1}' for i in range(5)]
        num_lessons = [f'Lesson_{i + 1}' for i in range(10)]

        self.create_products(num_products)
        self.create_lessons(num_lessons, num_products)
        # self.create_lesson_views(num_lesson_views, num_lessons)
        # self.create_access(num_access, num_products)

        self.stdout.write(self.style.SUCCESS('Процесс созданния фейковых данных завершен.'))


    def create_products(self, num_products):

        for i in range(len(num_products)):
            owner = User.objects.filter(username='admin').first()
            name = num_products[i]
            href = f'/product/{i + 1}'
            Product.objects.create(
                owner=owner,
                name=name,
                href=href,
            )


    def create_lessons(self, num_lessons, num_products):
        product_list = [product for product in Product.objects.all()]

        for i in range(len(num_lessons)):
            name = num_lessons[i]
            href = f'/lesson/{i + 1}'
            view_duration_seconds = random.randint(600, 6000)  # Длительность просмотра в секундах
            lesson = Lesson.objects.create(
                name=name,
                href=href,
                view_duration=view_duration_seconds
            )
            lesson.products.set(random.sample(product_list, 3))


    #         for _ in range(random.randint(1, len(num_products))):
    #             product = random.choice(Product.objects.all())
    #             lesson.products.add(product)
    #
    # def create_lesson_views(self, num_views, num_lessons):
    #     for _ in range(num_views):
    #         viewed = random.choice(['Просмотрено', 'Не просмотрено'])
    #         if viewed == 'Не просмотрено':
    #             viewing_time = None
    #         else:
    #             viewing_time = timezone.now() - timedelta(days=random.randint(1, 365))
    #
    #         lesson = random.choice(Lesson.objects.all())
    #         user = random.choice(User.objects.all())
    #         viewing_time = viewing_time
    #         viewed = viewed
    #         LessonView.objects.create(
    #             lesson=lesson,
    #             user=user,
    #             viewing_time=viewing_time,
    #             viewed=viewed
    #         )
    #
    # def create_access(self, num_access, num_products):
    #     for _ in range(num_access):
    #         user = random.choice(User.objects.all())
    #         product = random.choice(Product.objects.all())
    #         Access.objects.create(user=user, product=product)
    #
    #

