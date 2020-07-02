from django.test import TestCase
from accounts.forms import UserLoginForm, UserRegistrationFrom, ProfileForm
from datetime import datetime, timedelta


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
        self.assertEqual(form.errors['username'], [u'That username is already registered.'])

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


class TestProfileFrom(TestCase):
    """
    Tests for Profile Form
    """

    def test_profile_tests(self):
        # check birthdate must be in past
        ten_years = datetime.today() - timedelta(days=10*365)
        nine_years = ten_years + timedelta(days=3)
        future = datetime.now() + timedelta(days=10)

        # birth_date can't be in future
        form = ProfileForm({
            'birth_date': future,
            })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['birth_date'], [u'Please enter a valid birth date.'])

        # birth_date can't be 9 years adn 364 days
        form = ProfileForm({
            'birth_date': nine_years,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['birth_date'], [u'You must be 10 years or older to use this platform.'])

        # birth_date needs to be 10 years or greater
        form = ProfileForm({
            'birth_date': ten_years,
        })
        self.assertTrue('birth_date' not in form.errors)