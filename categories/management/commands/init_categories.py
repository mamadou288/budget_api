from django.core.management.base import BaseCommand
from categories.defaults import DEFAULT_CATEGORIES
from categories.models import Category

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        created = 0
        skipped = 0

        for name, category_type in DEFAULT_CATEGORIES:
            exists = Category.objects.filter(
                user__isnull=True,
                name=name,
                type=category_type,
            ).exists()

            if exists:
                skipped += 1
                continue

            Category.objects.create(
                user=None,
                name=name,
                type=category_type,
            )
            created += 1

        self.stdout.write(f"init_categories: created={created}, skipped={skipped}")


