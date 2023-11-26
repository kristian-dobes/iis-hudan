from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth.models import User
from .services import group_create, group_get_by_id, group_edit, group_get_threads, group_is_user_administrator
from .models import Profile


class CreateAdminTest(TestCase):
    
   def test_create_admin(self):
        # Assuming your create_admin command takes a username and password
        username = 'adminuser'
        password = 'adminpass'

        # Call the custom command to create an admin user
        call_command('register_admin', username, password, password)

        # Retrieve the profile associated with the user
        profile = Profile.objects.get(username='boi')

        # Check that the profile's is_admin field is True
        self.assertTrue(profile.is_admin, 'Profile should have is_admin set to True')