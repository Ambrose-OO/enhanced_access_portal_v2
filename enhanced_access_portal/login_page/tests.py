from django.test import TestCase

# Create your tests here.
class LoginPageTests(TestCase):
    def test_login_page_loads(self):
        response = self.client.get('/login_page/')
        self.assertEqual(response.status_code, 200)