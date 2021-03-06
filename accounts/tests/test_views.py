from django.test import TestCase, RequestFactory, Client
from django.contrib import auth
from users.models import User
from datetime import datetime, timedelta
from django.core.management import call_command


class TestUnauthorizedViews(TestCase):

    # @classmethod
    # # setup objects for testing
    # def setUp(cls):

    # test home page can be hit and that user is not logged in
    def test_get_home_page(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'index.html')
        self.assertContains(page, 'Register')
        self.assertContains(page, 'Login')


class TestRegisterUser(TestCase):

    def test_register(self):
        # register user with good credentials, user moves to home page
        page = self.client.post('/accounts/register/', {
            'email': 'testing@test.com',
            'password1': 'tester_pw_1',
            'password2': 'tester_pw_1'
        }, follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'index.html')
        self.assertContains(page, 'You have successfully registered.')
        self.assertContains(page, 'Logout')

        # check user has profile
        user = auth.get_user(self.client)
        self.assertEqual(user.email, "testing@test.com")


class TestLogin(TestCase):

    @classmethod
    # setup objects for testing
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='test@email.com', password="testing321"
        )

    def test_logout(self):
        # register user with good credentials, user moves to home page
        page = self.client.post('/accounts/register/', {
            'email': 'testing@test.com',
            'password1': 'tester_pw_1',
            'password2': 'tester_pw_1'
        }, follow=True)
        # logout user, should go to home page, no user in session
        page = self.client.post('/accounts/logout/', follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'index.html')
        self.assertContains(page, 'Login')
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_fail(self):
        # attempt to login with bad password
        page = self.client.post('/accounts/login/', {
            'email': 'test@email.com',
            'password': 'tester_pw_1111',
        }, follow=True)
        self.assertContains(page, "Email and/or password not valid.")

    def test_login_via_email(self):
        # login user with email, no next parameter, expectation is user goes to challenges page
        page = self.client.post('/accounts/login/', {
            'email': 'test@email.com',
            'password': 'testing321',
        }, follow=True)

        self.assertTemplateUsed(page, 'index.html')
        self.assertContains(page, 'You have successfully logged in')
        user = auth.get_user(self.client)

    def test_resigter_already_logged_in_redirects(self):
        # authenticated user if tries to go to login page goes back to challenges page

        page = self.client.post('/accounts/login/', {
            'email': 'test@email.com',
            'password': 'testing321',
        }, follow=True)

        # user that is authenticated tries to go to register page should be redirected to challenges page
        page = self.client.get('/accounts/register/', follow=True)
        self.assertContains(page, 'You are already a registered user')
        self.assertTemplateUsed(page, 'index.html')
