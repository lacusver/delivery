from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("service_delivery", "0001_initial"),
    ]

    def generate_superuser(apps, schema_editor):
        from django.contrib.auth.models import User

        superuser = User.objects.create_superuser(
            username=settings.DJANGO_SUPERUSER_USERNAME,
            email=settings.DJANGO_SUPERUSER_EMAIL,
            password=settings.DJANGO_SUPERUSER_PASSWORD,
        )

        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]
