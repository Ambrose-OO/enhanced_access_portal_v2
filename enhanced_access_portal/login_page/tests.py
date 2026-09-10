from django.test import TestCase
from django.contrib.auth.hashers import check_password
from login_page.models import User


# Create your tests here.
class LoginPageTests(TestCase):
    def test_login_page_loads(self):
        response = self.client.get('/login_page/')
        self.assertEqual(response.status_code, 200)
class PasswordStorageTests(TestCase):
    def test_password_is_not_stored_in_plain_text(self):
        self.client.post('/register_request/', {
            'first_name': 'Test',
            'other_names': 'User',
            'email_address': 'hashtest@example.com',
            'password': 'SubmittedPassword123',
            'password_repeat': 'SubmittedPassword123',
        })

        user = User.objects.get(emailaddress='hashtest@example.com')

        self.assertNotEqual(user.password, 'SubmittedPassword123')
        self.assertTrue(check_password('SubmittedPassword123', user.password))