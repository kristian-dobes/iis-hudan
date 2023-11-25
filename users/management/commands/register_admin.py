from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from users.models import Profile


class Command(BaseCommand):
    help = 'Register a new user'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('username', type=str, help='The username of the new user')
        parser.add_argument('password', type=str, help='The password for the new user')
        parser.add_argument('password2', type=str, help='The password again for confirmation')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        password2 = options['password2']
        # Your user_register logic here
        try:
            user = Profile.objects.get(username=username)
            self.stdout.write(self.style.ERROR('User already exists.'))
            return False
        except Profile.DoesNotExist:
            if password != password2:
                #self.stdout.write(self.style.ERROR('Passwords do not match.'))
                return False
            else:
                # Ensure you use Django's make_password to properly hash the password
                user = Profile.objects.create(username=username, password=make_password(password), is_admin = True)
                #self.stdout.write(self.style.SUCCESS(f'Successfully created user {username}'))
                return True