from django import forms
from .models import Task, Hint, Place, UserSubmission, AdminSubmission
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class UserSubmissionForm(forms.ModelForm):
    task_text = forms.CharField(max_length=200, label='Hunt Name')
    class Meta:
        model = UserSubmission
        fields = ['task_text', 'hint1', 'hint2', 'hint3',
                  'description', 'difficulties', ]  # Don't have approved here because it's not for users


class AdminSubmissionForm(forms.ModelForm):
    task_text = forms.CharField(max_length=200, label='Hunt Name')
    class Meta:
        model = AdminSubmission
        fields = ['task_text', 'hint1', 'hint2', 'hint3',
                  'description', 'latitude','longitude',
                  'facts','image','difficulties']  # Don't have approved here because it's not for users


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_text']


class HintForm(forms.ModelForm):
    hint1 = forms.CharField(label='Hint 1', max_length=200)
    hint2 = forms.CharField(label='Hint 2', max_length=200)
    hint3 = forms.CharField(label='Hint 3', max_length=200)

    class Meta:
        model = Hint
        fields = []


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['description', ]


class UsernameChangeForm(forms.Form):
    new_username = forms.CharField(label='New Username', max_length=150, required=True)


'''class DifficultyForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = UserSubmission
        fields = ['roles']'''
class TaskImageForm(forms.ModelForm):
    class Meta:
        model = Task  # Or Place
        fields = ['image']
