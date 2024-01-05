from django.contrib import admin
from .models import Task, Hint, Place, UserSubmission, Difficulty, UserProfile, UserTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_text',)


@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    list_display = ('hint_text',)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('description', 'latitude', 'longitude')


@admin.register(Difficulty)
class DifficultyAdmin(admin.ModelAdmin):
    list_display = ('description',)


@admin.register(UserSubmission)
class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'task_text',
        'hint1',
        'hint2',
        'hint3',
        'description',
        'approved'
    )
    list_filter = ('approved', 'task_text', 'description')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture')

@admin.register(UserTask)
class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'started', 'completed')
    list_filter = ('started', 'completed')
    search_fields = ('user__username', 'task__task_text')