from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group, User, Permission, AbstractUser



class CustomUserManager(BaseUserManager):

    def create_staffuser(self, username, password=None):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        # user = self.create_user(
        #         username = username,
        #         is_staff = True
        # )
        user = self.model(
            username=username,
            **extra_fields
        )
        staff_group, created = Group.objects.get_or_create(name="Staff")
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        user = self.model(
            email=email,
            **extra_fields
        )

        admin_group, created = Group.objects.get_or_create(name="Admin")
        staff_group, created = Group.objects.get_or_create(name="Staff")

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        user.set_password(password)
        user.save()
        return user
