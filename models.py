from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

design_choice = (
    ('', '-----Select Designationr-----'),
    ('Manager', 'Manager'),
    ('Team lead', 'Team Lead'),
    ('Developer', 'Developer')
)

status_choice = (
    ('Working on it', 'Working on it'),
    ('Stuck', 'Stuck'),
    ('Done', 'Done')
)


# ========== class-to-alter-user-table ==========

class new_user(AbstractUser):
    designation = models.CharField(
        max_length=30, choices=design_choice, default=False)
    profile = models.ImageField(default=False, upload_to='avatars')


# ========== class-to-generate-task-table ==========

class Task(models.Model):
    unique_user = models.ForeignKey(new_user, on_delete=models.CASCADE)
    tasktitle = models.CharField(max_length=30)
    taskDesc = models.TextField(blank=True)
    developer = models.CharField(max_length=30, blank=True)
    status = models.CharField(
        max_length=30, choices=status_choice, default='Working on it')
    created_time = models.DateField(auto_now_add=True)
    deadline = models.DateField(blank=True,null=True)


# ========== class-to-generate-contact-table ==========

class contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
