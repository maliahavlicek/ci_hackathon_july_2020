from django.test import TestCase
from accounts.forms import UserLoginForm, UserRegistrationFrom


class TestUserRegistrationFrom(TestCase):
    """
    Tests for User Registration
    """

    def test_register_user_tests(self):
        # verify you can create a uer by just passing in the user name and email
        form = UserRegistrationFrom({
            'email': 'testuser1@test.com',
            'username': 'test_user1',
            'password1': 'user_password_test_1',
            'password2': 'user_password_test_1'
        })
        self.assertTrue(form.is_valid())
        user1 = form.save()

        # verify that same username cannot be registered
        form = UserRegistrationFrom({
            'email': 'testuser2@test.com',
            'username': 'test_user1',
            'password1': 'user_password_test_1',
            'password2': 'user_password_test_1'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [u'A user with that username already exists.'])

        # verify that same email cannot be registered
        form = UserRegistrationFrom({
            'email': 'testuser1@test.com',
            'username': 'test',
            'password1': 'test',
            'password2': 'test'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [u'That email address is already registered.'])

        # verify that password can't be too similar to user name
        form = UserRegistrationFrom({
            'email': 'testuser2@test.com',
            'username': 'test_user2',
            'password1': 'test_user2',
            'password2': 'test_user2'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], [u'Your username cannot be part of your password.'])

        # verify that password can't be email
        form = UserRegistrationFrom({
            'email': 'testuser2@test.com',
            'username': 'test_user2',
            'password1': 'testuser2@test.com',
            'password2': 'testuser2@test.com'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], [u'Your email cannot be part of your password.'])

        # verify you have to confirm password
        form = UserRegistrationFrom({
            'email': 'testuser2@test.com',
            'username': 'test_user2',
            'password1': 'test_user2@test.com'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password2'], [u'This field is required.'])

        # verify you have to confirm password
        form2 = UserRegistrationFrom({
            'email': 'testuser2@test.com',
            'username': 'test_user2',
            'password2': 'test_user2@test.com',
        })
        self.assertFalse(form2.is_valid())
        self.assertEqual(form2.errors['password2'], [u'Passwords must match.'])

        # verify passwords match
        form2 = UserRegistrationFrom({
            'email': 'testuser2@test.com',
            'username': 'test_user2',
            'password1': 'testuser_2',
            'password2': 'testuser'
        })
        self.assertFalse(form2.is_valid())
        self.assertEqual(form2.errors['password2'], [u'Passwords must match.'])


class TestUserLoginForm(TestCase):
    """
    Tests for User Login
    """

    def test_user_login_tests(self):
        # form requires password
        form = UserLoginForm({
                'username': 'testtest_user1'
            })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'], [u'This field is required.'])

        # form requires username
        form = UserLoginForm({
                'password': 'testtest_user1'
            })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], [u'This field is required.'])
