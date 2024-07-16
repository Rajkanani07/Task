# Generated by Django 5.0.6 on 2024-07-16 10:37

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User_Details",
            fields=[
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(max_length=30)),
                ("last_name", models.CharField(max_length=30)),
                (
                    "username",
                    models.CharField(
                        max_length=20,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Username cannot contain the '@', '&', or '#' symbols.",
                                regex="^[^@&#]+$",
                            )
                        ],
                    ),
                ),
                (
                    "email_id",
                    models.EmailField(
                        max_length=50,
                        unique=True,
                        validators=[
                            django.core.validators.EmailValidator(
                                message="Invalid email format"
                            )
                        ],
                    ),
                ),
                (
                    "mobile_number",
                    models.CharField(
                        max_length=10,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Mobile number must be a 10-digit number starting with 6, 7, 8, or 9.",
                                regex="^[6-9]\\d{9}$",
                            )
                        ],
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Password must contain at least 8 characters, including at least one digit, one lowercase letter, and one uppercase letter.",
                                regex="^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$",
                            )
                        ],
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("m", "Male"), ("f", "Female")], max_length=1
                    ),
                ),
                ("date_of_birth", models.DateField()),
                ("is_mobile_verified", models.BooleanField(default=False)),
                ("is_email_verified", models.BooleanField(default=False)),
                ("is_user_login", models.BooleanField(default=False)),
                ("is_blocked", models.BooleanField(default=False)),
                ("block_expiration", models.DateTimeField(blank=True, null=True)),
                ("last_login", models.DateTimeField(blank=True, null=True)),
                ("unsuccessful_attempts", models.IntegerField(default=0)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("is_user_login", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
