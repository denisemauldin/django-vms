from test_plus.test import TestCase

from ..forms import SignupForm
from .factories import UserFactory

class TestSignupForm(TestCase):
    user_factory = UserFactory

    def setUp(self):
        self.user = self.make_user('notalamode', 'notalamodespassword')

    def test_clean_username_success(self):
        # Instantiate the form with a new username
        form = SignupForm({
            'username': 'alamode',
            'name': 'al mode',
            'member_number': 39,
            'password1': '7jefB#f@Cc7YJB]2v',
            'password2': '7jefB#f@Cc7YJB]2v',
        })
        # Run is_valid() to trigger the validation
        valid = form.is_valid()
        self.assertTrue(valid)

        # Run the actual clean_username method
        username = form.clean_username()
        self.assertEqual('alamode', username)

    def test_clean_username_false(self):
        # Instantiate the form with the same username as self.user
        form = SignupForm({
            'username': self.user.username,
            'name': 'al mode',
            'member_number': 39,
            'password1': 'notalamodespassword',
            'password2': 'notalamodespassword',
        })
        # Run is_valid() to trigger the validation, which is going to fail
        # because the username is already taken
        valid = form.is_valid()
        self.assertFalse(valid)

        # The form.errors dict should contain a single error called 'username'
        self.assertTrue(len(form.errors) == 1)
        self.assertTrue('username' in form.errors)
