from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Task(models.Model):
    task_text = models.CharField(max_length=200)
    approved_status = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    completed_by = models.ManyToManyField(User, related_name='completed_tasks')
    image = models.ImageField(upload_to='tasks_images/', null=True, blank=True)
    def __str__(self):
        return self.task_text


class Hint(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    hint_text = models.CharField(max_length=2000)

    def __str__(self):
        return self.hint_text


# https://www.youtube.com/watch?v=fsVY66QBhwM for image stuff
class Place(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='location_images/', null=True, blank=False)
    image = models.ImageField(upload_to='location_pictures/', null=True, blank=False)
    facts = models.TextField(max_length=100000, null=True, blank=True)


class UserSubmission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied')
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    DIFFICULTY_CHOICES = [('easy', "EASY"),
                          ('medium', "MEDIUM"),
                          ('hard', "HARD")]

    difficulties = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy')

    task_text = models.CharField(max_length=200, blank=False, null=True)
    hint1 = models.CharField(max_length=200, blank=False, null=True)
    hint2 = models.CharField(max_length=200, blank=False, null=True)
    hint3 = models.CharField(max_length=200, blank=False, null=True)
    description = models.CharField(max_length=200, blank=False, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    # image = models.ImageField(upload_to='staticfiles/location_images', null=True, blank=False)
    # facts = models.TextField(max_length=100000, blank=False, null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return "User Submission: {self.id}, {self.task_text}"


class AdminSubmission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied')
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    DIFFICULTY_CHOICES = [('easy', "EASY"),
                          ('medium', "MEDIUM"),
                          ('hard', "HARD")]

    difficulties = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy')

    task_text = models.CharField(max_length=200, blank=False, null=True)
    hint1 = models.CharField(max_length=200, blank=False, null=True)
    hint2 = models.CharField(max_length=200, blank=False, null=True)
    hint3 = models.CharField(max_length=200, blank=False, null=True)
    description = models.CharField(max_length=200, blank=False, null=True)
    latitude = models.FloatField(null=True, blank=False)
    longitude = models.FloatField(null=True, blank=False)
    image = models.ImageField(upload_to='location_pictures/', null=True, blank=True)
    facts = models.CharField(max_length=200, blank=True, null=True)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return "User Submission: {self.id}, {self.task_text}"







class Difficulty(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    description = models.CharField(max_length=10)
    difficulty = models.CharField(max_length=10, choices=UserSubmission.DIFFICULTY_CHOICES, default='easy')

    def __str__(self):
        return self.description

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='images/default-avatar.png')

    def __str__(self):
        return self.user.username
class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    started = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'task')