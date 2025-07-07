from django.test import TestCase
from django.contrib.auth import get_user_model


# Create your tests here.


class usersManagersTest(TestCase):
    """Test class for custom users model"""

    def test_create_user_with_email(self):
        """
        Test creating a user
        """
        User = get_user_model()
        test_user = User.objects.create_user(
            email="johnDoe@example.com", password="foo"
        )

        self.assertEqual(test_user.email, "johnDoe@example.com")
        self.assertTrue(test_user.is_active)
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)

    def test_create_user_without_email(self):
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="foo")

    def test_create_user_invalid_email_format(self):
        """
        Test that creating a user with an invalid email format raises a ValueError.
        """
        User = get_user_model()
        invalid_emails = [
            "invalid-email",
            "user@.com",
            "user@com",
            "user@example",
            "user@example.",
            "user@example..com",
            "user@example.c",  # too short TLD
            "user@example.com.",
            "@example.com",
            "user@example.com@",
            "user name@example.com",  # space in local part
            "user@example com",  # space in domain
        ]

        for email in invalid_emails:
            with self.assertRaises(ValueError):
                User.objects.create_user(email=email, password="password123")

    def test_create_superuser(self):
        """
        Test that a superuser can be created successfully.
        """
        User = get_user_model()
        email = "admin@example.com"
        password = "admin-password-123"
        admin_user = User.objects.create_superuser(email=email, password=password)

        self.assertEqual(admin_user.email, email)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.check_password(password))

    def test_create_superuser_is_staff_false(self):
        """
        Test that creating a superuser with is_staff=False raises a ValueError.
        """
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="test@example.com", password="password123", is_staff=False
            )

    def test_create_superuser_is_superuser_false(self):
        """
        Test that creating a superuser with is_superuser=False raises a ValueError.
        """
        User = get_user_model()
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="test@example.com", password="password123", is_superuser=False
            )

    def test_create_user_is_superuser_false(self):
        """
        Test that creating a user with is_superuser not possible.
        """
        User = get_user_model()
        test_user = User.objects.create_user(
            email="test@example.com", password="pass123", is_superuser=True
        )
        self.assertFalse(test_user.is_superuser)

    def test_email_unique(self):
        """
        Test that email addresses are unique.
        """
        User = get_user_model()
        email = "duplicate@example.com"
        User.objects.create_user(email=email, password="password123")
        with self.assertRaises(Exception):  # IntegrityError or similar from DB
            User.objects.create_user(email=email, password="anotherpassword")
