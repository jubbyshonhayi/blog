from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from users.models import Profile


class Command(BaseCommand):
    help = "Create Profile rows for users that do not have one."

    def handle(self, *args, **options):
        created_count = 0

        for user in User.objects.all():
            _, created = Profile.objects.get_or_create(user=user)
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Created {created_count} missing profile(s).")
        )
