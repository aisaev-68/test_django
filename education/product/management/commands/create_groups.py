from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission, User
from mimesis import Person
from mimesis.locales import Locale

from education import settings
from product.models import Product, Lesson, LessonView, Access



class Command(BaseCommand):
    help = 'Creates read only default permission groups for users'

    def handle(self, *args, **options):
        self.stdout.write("Create groups")
        admin_group, created = Group.objects.get_or_create(name="Admin")
        clients_group, created = Group.objects.get_or_create(name="Clients")

        content_type_product = ContentType.objects.get_for_model(Product)
        product_permission = Permission.objects.filter(content_type=content_type_product)
        for perm in product_permission:
            admin_group.permissions.add(perm)

            if perm.codename == "view_product":
                clients_group.permissions.add(perm)

        content_type_lesson = ContentType.objects.get_for_model(Lesson)
        lesson_permission = Permission.objects.filter(content_type=content_type_lesson)
        for perm in lesson_permission:
            admin_group.permissions.add(perm)
            if perm.codename == "view_lesson":
                clients_group.permissions.add(perm)

        content_type_lesson_view = ContentType.objects.get_for_model(LessonView)
        lesson_view_permission = Permission.objects.filter(content_type=content_type_lesson_view)
        for perm in lesson_view_permission:
            admin_group.permissions.add(perm)
            if perm.codename == "view_lesson_view":
                clients_group.permissions.add(perm)

        content_type_access = ContentType.objects.get_for_model(Access)
        access_permission = Permission.objects.filter(content_type=content_type_access)
        for perm in access_permission:
            admin_group.permissions.add(perm)
            if perm.codename == "view_access":
                clients_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS("Groups created"))
        self.stdout.write(self.style.SUCCESS("Create superuser"))
        User.objects.create_superuser(
            username=settings.SUPER_USER,
            email=settings.SUPERUSER_EMAIL,
            password=settings.SUPERUSER_PASSWORD,
        )
        admin_user = User.objects.create_user(
            username=settings.USER_ADMIN,
            email=settings.EMAIL,
            password=settings.PASSWORD,
            is_staff=True,
        )
        admin_group = Group.objects.get(name="Admin")
        admin_user.groups.add(admin_group)
        self.stdout.write(self.style.SUCCESS(f"{admin_user} added in Admin group"))

        for _ in range(10):
            person = Person(locale=Locale.RU)
            client_user = User.objects.create_user(
                username=person.username(),
                email=person.email(),
                password='12345',
            )

            client_group = Group.objects.get(name="Clients")
            client_user.groups.add(client_group)

            self.stdout.write(self.style.SUCCESS(f"{client_user} added in Clients group"))

        self.stdout.write(self.style.SUCCESS("Process end successful."))
