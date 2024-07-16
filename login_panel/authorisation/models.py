from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.hashers import make_password, check_password


# Create your models here.


class User_Details(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(null=False, max_length=30)
    last_name = models.CharField(null=False, max_length=30)
    username = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
        validators=[
            validators.RegexValidator(
                regex=r'^[^@&#]+$',  # This ensures that the '@', '&', and '#' symbols are not present.
                message="Username cannot contain the '@', '&', or '#' symbols."
            ),
        ],
    )
    email_id = models.EmailField(
        max_length=50,
        null=False,
        unique=True,
        validators=[validators.EmailValidator(message="Invalid email format")],
    )
    mobile_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=r"^[6-9]\d{9}$",
                message="Mobile number must be a 10-digit number starting with 6, 7, 8, or 9.",
            )
        ],
    )
    password = models.CharField(
        max_length=100,
        validators=[
            validators.RegexValidator(
                regex=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$",
                message="Password must contain at least 8 characters, including at least one digit, one lowercase letter, "
                        "and one uppercase letter.",
            )
        ],
    )
    gender = models.CharField(
        max_length=1, choices=(("m", "Male"), ("f", "Female")), null=False
    )
    date_of_birth = models.DateField()
    is_mobile_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_user_login = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    block_expiration = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    unsuccessful_attempts = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=True)
    is_deleted = models.BooleanField(default=False)


    # def save(self, *args, **kwargs):
    #     if self.password:
    #         self.password = make_password(self.password)
    #     super().save(*args, **kwargs)

    # def is_password_valid(self, raw_password):
    #     return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        # if self.password:
        #     self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def is_password_valid(self, raw_password):
        return self.password == (raw_password)
    

class CustomUser(AbstractUser):
    is_user_login = models.BooleanField(default=False)

    def login(self, *args, **kwargs):
        if self.is_user_login:
            raise ValueError("User is already logged in.")
        else:
            self.is_user_login = True
            self.save()
            return super().login(*args, **kwargs)

    def logout(self, *args, **kwargs):
        if not self.is_user_login:
            raise ValueError("User is already logged out.")
        else:
            self.is_user_login = False
            self.save()
            return super().logout(*args, **kwargs)


    # pass
