from django.test import TestCase, RequestFactory, Client
from accounts.models import User
from products.models import ServiceLevel
from django.contrib import auth
from accounts.models import Tag
from datetime import datetime, timedelta
from django.core.management import call_command
from accounts.views import user_profile


class TestUnauthorizedViews(TestCase):

    @classmethod
    # setup objects for testing
    def setUp(cls):
        product = ServiceLevel(
            name='Free',
            price=0.00,
            features=['group_emails', 'peer_ratings', 'submission_image'],
            description='Our Free Tier is perfect for a small group that wants to challenge each other. Throw the gauntlet down and see who comes up with the best response.',
            max_members_per_challenge=5,
            max_number_of_challenges=5,
            video_length_in_seconds=0,
            max_submission_size_in_MB=500,
            image='/images/products/hot-air-balloon.png'
        )
        product.save()

        # create a couple of tags
        Tag.objects.create(
            name='Sports',
        )
        Tag.objects.create(
            name='Music',
        )

    # test home page can be hit and that user is not logged in
    def test_get_home_page(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'index.html')
        self.assertContains(page, 'Register')
        self.assertContains(page, 'Login')
        self.assertNotContains(page, 'My Account')

    # test that unauthenticated user can get to products page
    def test_get_product_page(self):
        page = self.client.get("/products/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'products.html')
        # verify Free Product is present and user has checkout button
        self.assertContains(page, '/checkout/1/')
        self.assertContains(page, 'Register')
        self.assertContains(page, 'Login')
        self.assertNotContains(page, 'My Account')


class TestAuthenticationRequiredViews(TestCase):
    # setup objects for testing

    @classmethod
    def setUp(cls):
        product = ServiceLevel(
            name='Free',
            price=0.00,
            features=['group_emails', 'peer_ratings', 'submission_image'],
            description='Our Free Tier is perfect for a small group that wants to challenge each other. Throw the gauntlet down and see who comes up with the best response.',
            max_members_per_challenge=5,
            max_number_of_challenges=5,
            video_length_in_seconds=0,
            max_submission_size_in_MB=500,
            image='/images/products/hot-air-balloon.png'
        )
        product.save()

        # create a couple of tags
        Tag.objects.create(
            name='Sports',
        )
        Tag.objects.create(
            name='Music',
        )

        User.objects.create(
            username='alreadyUsed',
            email='alreadyUsed@test.com',
            password="testing_1234",
        )

    def test_unauthenticated_checkout_redirects(self):
        # user is redirected to login before checking out
        page = self.client.get("/checkout/1/")
        self.assertRedirects(page, '/accounts/login/?next=/checkout/1/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

        # post invalid input and verify next page is still in response and was posted
        page = self.client.post('/accounts/login/?next=/checkout/1/', {
            'email': 'testing_1@test.com',
            'username': 'testing_1',
            'password1': 'test_pass_1',
            'password2': 'test_pass_1',
            'next': '/checkout/1/'
        }, follow=True)
        self.assertEquals(page.wsgi_request.POST['next'], '/checkout/1/')
        self.assertContains(page, '<input type="hidden" name="next" value="/checkout/1/" id="id_next">')

    def test_unauthenticated_account_overview_redirects(self):
        # has to login before seeing profile
        page = self.client.get("/accounts/profile/")
        self.assertEqual(page.status_code, 302)
        self.assertRedirects(page, '/accounts/login/?next=/accounts/profile/')

    def test_unauthenticated_update_profile_redirects(self):
        # has to login before updating profile
        page = self.client.get("/accounts/profile/update/")
        self.assertEqual(page.status_code, 302)
        self.assertRedirects(page, '/accounts/login/?next=/accounts/profile/update/')

    def test_unauthenticated_challenges_redirects(self):
        # has to login before getting to challenges
        page = self.client.get("/challenges/")
        self.assertEqual(page.status_code, 302)
        self.assertRedirects(page, '/accounts/login/?next=/challenges/')

    def test_unauthenticated_update_user_redirects(self):
        # user is redirected to login before updating user info
        page = self.client.get("/accounts/user/update/", follow=True)
        self.assertRedirects(page, '/accounts/login/?next=/accounts/user/update/', status_code=302,
                             target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)


class TestRegisterUser(TestCase):

    def test_register_fails_too_similar_password(self):
        # first register a user with too similar of password, user remains on registration page
        page = self.client.post('/accounts/register/', {
            'email': 'testing@test.com',
            'username': 'test_1',
            'password1': 'test_pass_1',
            'password2': 'test_pass_1'
        }, follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'registration.html')
        self.assertContains(page, 'The password is too similar to the username')

    def test_register(self):
        # register user with good credentials, user moves to home page
        page = self.client.post('/accounts/register/', {
            'email': 'testing@test.com',
            'username': 'this_is_test_1',
            'password1': 'tester_pw_1',
            'password2': 'tester_pw_1'
        }, follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'index.html')
        self.assertContains(page, 'You have successfully registered.')
        self.assertContains(page, 'Products')
        self.assertContains(page, 'Challenges')
        self.assertContains(page, 'My Account')

        # check user has profile
        user = auth.get_user(self.client)
        self.assertEqual(user.profile.product_level, ServiceLevel.objects.first())


class TestUpdateUser(TestCase):

    @classmethod
    def setUp(self):
        # set up 3 base products from json
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@email.com', password="testing_1234"
        )
        # tie Free product to user
        self.user.profile.get_product_level()

        # setup another user
        User.objects.create(
            username='alreadyUsed',
            email='alreadyUsed@test.com',
            password="testing_1234",
        )

    def test_update_user_page(self):
        # login user and goto update user page
        self.client.login(username='testuser', password="testing_1234")
        user = auth.get_user(self.client)
        page = self.client.get('/accounts/user/update/')

        # verify user is on expected page
        self.assertTemplateUsed('user_update.html')
        self.assertContains(page, 'Updating User Info')
        # verify user details are as expected
        self.assertContains(page, "testuser")
        self.assertEqual('testuser', user.username)
        self.assertContains(page, "test@email.com")
        self.assertEqual('test@email.com', user.email)

    def test_update_first_name(self):
        # update first name

        # login user and goto update user page
        self.client.login(username='testuser', password="testing_1234")
        user = auth.get_user(self.client)
        page = self.client.post('/accounts/user/update/', {
            'email': user.email,
            'username': user.username,
            'first_name': "joe",
            'last_name': '',
        }, follow=True)
        self.assertEqual(page.status_code, 200)

        # verify user goes to profile page
        self.assertTemplateUsed('profile.html')
        self.assertContains(page, 'Account Overview')
        # verify user's first name was updated
        self.assertContains(page, "test@email.com")
        self.assertContains(page, "joe")

    def test_username_takeover_prevented(self):
        # try to take over AlreadyUser username

        # login user and goto update user page
        self.client.login(username='testuser', password="testing_1234")
        user = auth.get_user(self.client)
        page = self.client.post('/accounts/user/update/', {
            'email': user.email,
            'username': "alreadyUsed",
            'first_name': "joe",
            'last_name': '',
        }, follow=True)
        # verify user is on expected page
        self.assertTemplateUsed('user_update.html')
        self.assertContains(page, 'Updating User Info')
        self.assertContains(page, 'A user with that username already exists.')

    def test_email_takeover_prevented(self):
        # try to take over AlreadyUser username

        # login user and goto update user page
        self.client.login(username='testuser', password="testing_1234")
        user = auth.get_user(self.client)
        # try to take over AlreadyUser email
        page = self.client.post('/accounts/user/update/', {
            'username': user.username,
            'email': "alreadyUsed@test.com",
            'first_name': "joe",
            'last_name': '',
        }, follow=True)
        # verify user is on expected page
        self.assertTemplateUsed('user_update.html')
        self.assertContains(page, 'Updating User Info')
        self.assertContains(page, 'That email is already in use.')

    def test_update_last_name(self):
        # update first name

        # login user and goto update user page
        self.client.login(username='testuser', password="testing_1234")
        user = auth.get_user(self.client)
        # update last name
        page = self.client.post('/accounts/user/update/', {
            'email': user.email,
            'username': user.username,
            'first_name': "joe",
            'last_name': 'cool',
        }, follow=True)
        self.assertEqual(page.status_code, 200)
        # verify user goes to profile page
        self.assertTemplateUsed('profile.html')
        self.assertContains(page, 'Account Overview')
        # verify user's first name was updated
        self.assertContains(page, "test@email.com")
        self.assertContains(page, "joe")
        self.assertContains(page, "cool")
        self.assertContains(page, "testuser")

        user = auth.get_user(self.client)
        self.assertEqual('test@email.com', user.email)
        self.assertEqual('testuser', user.username)
        self.assertEqual(user.first_name, "joe")
        self.assertEquals(user.last_name, "cool")


class TestProfile(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@email.com', password="testing321"
        )

    def test_profile_view_logged_in(self):
        request = self.factory.get('/')
        request.user = self.user
        response = user_profile(request)

        self.assertEqual(response.status_code, 200)

    def test_profile_update_view_logged_in(self):
        client = Client()
        client.login(username='testuser', password="testing321")

        response = client.get('/accounts/profile/update/')
        form = response.context['profile_form']

    def test_profile_update_too_young_by_few_days(self):
        client = Client()
        client.login(username='testuser', password="testing321")

        response = client.get('/accounts/profile/update/')
        # post to profile with too young of birthday
        page = client.post('/accounts/profile/update/', {
            'profile_pic': 'accounts/fixtures/profile2.png',
            'birth_date': (datetime.now() - timedelta(days=3000)).date(),
            'tags': [],
        }, follow=True)
        self.assertContains(page, 'You must be 10 years or older to use this platform.')

    def test_profile_update_too_young_not_born(self):
        client = Client()
        client.login(username='testuser', password="testing321")

        response = client.get('/accounts/profile/update/')
        # post to profile with too young of birthday
        page = client.post('/accounts/profile/update/', {
            'profile_pic': 'accounts/fixtures/profile2.png',
            'birth_date': (datetime.now() + timedelta(days=3)).date(),
            'tags': [],
        }, follow=True)
        self.assertContains(page, 'Please enter a valid birth date.')

    def test_profile_update_success(self):
        client = Client()
        client.login(username='testuser', password="testing321")

        response = client.get('/accounts/profile/update/')

        # post to profile with all necessary data
        page = client.post('/accounts/profile/update/', {
            'profile_pic': 'accounts/fixtures/profile2.png',
            'birth_date': (datetime.now() - timedelta(days=3653)).date(),
            'tags': [],
        }, follow=True)
        self.assertContains(page, 'Your profile was successfully updated!')

        self.assertTemplateUsed(page, 'profile.html')


class TestLogin(TestCase):

    @classmethod
    # setup objects for testing
    def setUp(self):
        product = ServiceLevel(
            name='Free',
            price=0.00,
            features=['group_emails', 'peer_ratings', 'submission_image'],
            description='Our Free Tier is perfect for a small group that wants to challenge each other. Throw the gauntlet down and see who comes up with the best response.',
            max_members_per_challenge=5,
            max_number_of_challenges=5,
            video_length_in_seconds=0,
            max_submission_size_in_MB=500,
            image='/images/products/hot-air-balloon.png'
        )
        product.save()

        # create a couple of tags
        Tag.objects.create(
            name='Sports',
        )
        Tag.objects.create(
            name='Music',
        )

        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@email.com', password="testing321"
        )

    def test_logout(self):
        # register user with good credentials, user moves to home page
        page = self.client.post('/accounts/register/', {
            'email': 'testing@test.com',
            'username': 'this_is_test_1',
            'password1': 'tester_pw_1',
            'password2': 'tester_pw_1'
        }, follow=True)
        # logout user, should go to home page, no user in session
        page = self.client.post('/accounts/logout/', follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'index.html')
        self.assertContains(page, 'Login')
        self.assertNotContains(page, 'My Account')
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertNotEqual(user.username, 'this_is_test_1')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_fail(self):
        # attempt to login with bad password
        page = self.client.post('/accounts/login/', {
            'username': 'test@email.com',
            'password': 'tester_pw_1111',
        }, follow=True)
        self.assertContains(page, "Username/email and password not valid.")

    def test_login_via_email(self):
        # login user with email, no next parameter, expectation is user goes to challenges page
        page = self.client.post('/accounts/login/', {
            'username': 'test@email.com',
            'password': 'testing321',
        }, follow=True)

        self.assertRedirects(page, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        self.assertTemplateUsed(page, 'challenges.html')
        self.assertContains(page, 'Challenges')
        self.assertContains(page, 'You have successfully logged in')
        user = auth.get_user(self.client)

    def test_login_already_logged_in_redirects(self):
        # authenticated user if tries to go to login page goes back to challenges page

        page = self.client.post('/accounts/login/', {
            'username': 'test@email.com',
            'password': 'testing321',
        }, follow=True)

        page = self.client.get('/accounts/login/', follow=True)
        self.assertRedirects(page, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        self.assertTemplateUsed(page, 'challenges.html')

    def test_resigter_already_logged_in_redirects(self):
        # authenticated user if tries to go to login page goes back to challenges page

        page = self.client.post('/accounts/login/', {
            'username': 'test@email.com',
            'password': 'testing321',
        }, follow=True)

        # user that is authenticated tries to go to register page should be redirected to challenges page
        page = self.client.get('/accounts/register/', follow=True)
        self.assertRedirects(page, '/challenges/', status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)
        self.assertContains(page, 'You are already a registered user')
        self.assertTemplateUsed(page, 'challenges.html')

    def test_login_with_next_in_respects_next_redirect(self):
        page = self.client.post('/accounts/login/?next=/accounts/profile/', {
            'username': 'test@email.com',
            'password': 'testing321',
            'next': '/accounts/profile',
        }, follow=True)
        self.assertTemplateUsed('profile.html')
