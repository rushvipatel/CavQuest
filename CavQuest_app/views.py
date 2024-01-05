from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm, HintForm, PlaceForm, UserSubmissionForm, UsernameChangeForm, AdminSubmissionForm
from .models import Hint, Task, Place, UserSubmission, Difficulty, UserProfile, UserTask,AdminSubmission
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.text import slugify
from django.http import HttpResponseForbidden, JsonResponse
from django.conf import settings
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib import messages

allowed_emails = [
        "umm9ef@virginia.edu",
    ]

@login_required
def user_profile(request):
    tasks = Task.objects.filter(approved_status=True)
    submissions = UserSubmission.objects.filter(approved=False)
    user_tasks = UserTask.objects.filter(user=request.user, completed=False, started=True)


    if (request.user.username == "cs3240.super" or request.user.email == "umm9ef@virginia.edu"):
        template_name = 'CavQuest_app/admin_profile.html'

    else:
        template_name = 'CavQuest_app/user_profile.html'
    completed_tasks = request.user.completed_tasks.all()
    context = {
        'user': request.user,
        'tasks': tasks,
        'submissions': submissions,
        'completed_tasks': completed_tasks,
        'user_tasks': user_tasks,
    }

    return render(request, template_name, context)


def index(request):
    is_admin = False
    return render(request, 'CavQuest_app/index.html', {'is_admin': is_admin})

def about(request):
    return render(request, 'CavQuest_app/about.html')


def homepage_loggedin(request):
    return render(request, 'CavQuest_app/homepage_loggedin.html')


def user_profile2(request):
    return render(request, 'CavQuest_app/user_profile2.html')


def admin(request):
    return render(request, "CavQuest_app/admin_profile.html")


def login(request):
    return render(request, "CavQuest_app/login.html")


def tutorial(request):
    return render(request, "CavQuest_app/tutorial.html")


def logout_view(request):
    logout(request)
    return redirect('index')


def task_list(request):
    tasks = Task.objects.filter(approved_status=True)
    return render(request, 'CavQuest_app/task_list.html', {'tasks': tasks})
def start_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    user_task, created = UserTask.objects.get_or_create(user=request.user, task=task)
    if not created:
        user_task.started = True
        user_task.save()
    return redirect('CavQuest_app:hunting', task_id=task.id)

def display_submissions(request):
    allowed_emails = [
        "umm9ef@virginia.edu",
    ]
    if request.user.email not in allowed_emails:
        return HttpResponseForbidden("You are not allowed to see this.")
    submissions = UserSubmission.objects.all()
    return render(request, 'CavQuest_app/display_submissions.html', {'submissions': submissions})


# https://www.django-rest-framework.org/api-guide/serializers/
def hunting(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    hints = Hint.objects.filter(task=task)
    hints_json = serializers.serialize('json', hints)
    place = Place.objects.filter(task=task)
    difficulty = Difficulty.objects.filter(task=task)
    task_info = {
        'task': task,
        'hints': hints,
        'place': place,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'difficulty': difficulty,
        'hints_json': hints_json,
    }
    return render(request, 'CavQuest_app/start_hunt.html', task_info)


def json_for_hunting(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    hints = Hint.objects.filter(task=task)
    place = Place.objects.filter(task=task)
    difficulty = Difficulty.objects.filter(task=task)

    # Serialize the task data to JSON
    task_info = {
        'task': task,
        'place': place,
        'hints': hints,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'difficulty': difficulty,
    }

    # Return the serialized data as JSON response
    return JsonResponse(task_info)


# Cite for the func: https://www.geeksforgeeks.org/get_object_or_404-method-in-django-models/
def task_details(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    hints = Hint.objects.filter(task=task)
    difficulty = Difficulty.objects.get(task=task)
    print("diff: ", difficulty)
    task_info = {
        'task': task,
        'hints': hints,
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'difficulty': difficulty,

    }
    return render(request, 'CavQuest_app/task_details.html', task_info)


def submission_details(request, submission_id):
    submission = get_object_or_404(UserSubmission, pk=submission_id)

    if request.method == 'POST':
        if 'approve' in request.POST:
            new_task = Task(
                task_text=submission.task_text,
                approved_status=True
            )
            new_hint1 = Hint(
                hint_text=submission.hint1,
                task=new_task
            )
            new_hint2 = Hint(
                hint_text=submission.hint2,
                task=new_task
            )
            new_hint3 = Hint(
                hint_text=submission.hint3,
                task=new_task,
            )
            new_place = Place(
                description=submission.description,
                task=new_task,
                latitude=request.POST.get('latitude'),
                longitude=request.POST.get('longitude'),
                image = request.FILES.get('image'),
                facts=request.POST.get('facts'),
            )
            new_difficulty = Difficulty(
                task=new_task,
                difficulty=submission.difficulties,
            )
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            image = request.FILES.get('image')
            facts = request.POST.get('facts')

            new_task.save()
            new_hint1.save()
            new_hint2.save()
            new_hint3.save()
            new_place.save()
            new_difficulty.save()

            # Update the UserSubmission instance to mark it as approved
            submission.approved = True
            submission.latitude = latitude
            submission.longitude = longitude
            submission.image = image
            submission.facts = facts
            submission.save()

            return redirect('CavQuest_app:display_submissions')

        # Check for the "Deny" action
        elif 'action' in request.POST and request.POST['action'] == 'deny':
            submission.delete()  # Assuming you want to delete the denied submission
            return redirect('CavQuest_app:display_submissions')

    submission_info = {
        'submission': submission,
        'task': submission.task_text,
        'hint1': submission.hint1,
        'hint2': submission.hint2,
        'hint3': submission.hint3,
        'place': submission.description,
        'difficulty': submission.difficulties,
        'approved': submission.approved,
        'latitude': submission.latitude,
        'longitude': submission.longitude,
    }
    return render(request, 'CavQuest_app/submission_details.html', submission_info)


def add(request):
    allowed_emails = [
        "umm9ef@virginia.edu",
    ]
    
    if request.user.email in allowed_emails:
        if request.method == 'POST':
            admin_submission_form = AdminSubmissionForm(request.POST, request.FILES)
            if admin_submission_form.is_valid():
                task_text = admin_submission_form.cleaned_data['task_text']
                hint1 = admin_submission_form.cleaned_data['hint1']
                hint2 = admin_submission_form.cleaned_data['hint2']
                hint3 = admin_submission_form.cleaned_data['hint3']
                description = admin_submission_form.cleaned_data['description']
                latitude=admin_submission_form.cleaned_data['latitude']
                longitude=admin_submission_form.cleaned_data['longitude']
                difficulty = admin_submission_form.cleaned_data['difficulties']
                image=admin_submission_form.cleaned_data['image']
                facts=admin_submission_form.cleaned_data['facts']
                
                admin_submission = AdminSubmission(
                    task_text=task_text,
                    hint1=hint1,
                    hint2=hint2,
                    hint3=hint3,
                    description=description,
                    latitude=latitude,
                    longitude=longitude,
                    difficulties=difficulty,
                    image=image,
                    facts=facts,
                    approved=True,
                )
                admin_submission.save()
                new_task = Task(
                task_text=admin_submission.task_text,
                approved_status=True
                )
                new_hint1 = Hint(
                    hint_text=admin_submission.hint1,
                    task=new_task
                )
                new_hint2 = Hint(
                    hint_text=admin_submission.hint2,
                    task=new_task
                )
                new_hint3 = Hint(
                    hint_text=admin_submission.hint3,
                    task=new_task,
                )
                new_place = Place(
                    description=admin_submission.description,
                    task=new_task,
                    latitude=latitude,
                    longitude=longitude,
                    image=request.FILES.get('image'),
                    facts=facts
                )
                new_difficulty = Difficulty(
                    task=new_task,
                    difficulty=admin_submission.difficulties,
                )
                new_task.save()
                new_hint1.save()
                new_hint2.save()
                new_hint3.save()
                new_difficulty.save()
                #location_picture = request.FILES.get('image')
                #new_place.image.save(location_picture.name, location_picture, save=True)
                new_place.save()
                return redirect('successful_submission')
        else:
            admin_submission_form = AdminSubmissionForm()
            return render(request, 'CavQuest_app/add.html', {'user_submission_form': admin_submission_form})
    else:
        if request.method == 'POST':
            user_submission_form = UserSubmissionForm(request.POST)
            if user_submission_form.is_valid():
                task_text = user_submission_form.cleaned_data['task_text']
                hint1 = user_submission_form.cleaned_data['hint1']
                hint2 = user_submission_form.cleaned_data['hint2']
                hint3 = user_submission_form.cleaned_data['hint3']
                description = user_submission_form.cleaned_data['description']
                difficulty = user_submission_form.cleaned_data['difficulties']

                user_submission = UserSubmission(
                    task_text=task_text,
                    hint1=hint1,
                    hint2=hint2,
                    hint3=hint3,
                    description=description,
                    difficulties=difficulty,
                    approved=False,
                )
                user_submission.save()
                return redirect('successful_submission')
        else:
            user_submission_form = UserSubmissionForm()
            return render(request, 'CavQuest_app/add.html', {'user_submission_form': user_submission_form})


def successful_submission(request):
    return render(request, 'CavQuest_app/successful_submission.html')


def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('CavQuest_app:task_list')


def deny_submission(request, submission_id):
    allowed_emails = [
        "umm9ef@virginia.edu",
    ]
    if request.user.username != "cs3240.super" and request.user.email not in allowed_emails:
        return HttpResponseForbidden("You don't have permission to access this.")

    submission = get_object_or_404(UserSubmission, pk=submission_id)
    submission.status = 'denied'
    submission.save()

    return redirect('user_profile')


def congratulations(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.completed_by.add(request.user)
    task.completed = True
    place = Place.objects.get(task=task)
    task.save()

    return render(request, 'CavQuest_app/congratulations.html', {'task': task, 'place': place})


def task_list(request):
    pending_tasks = Task.objects.filter(completed=False)
    completed_tasks = Task.objects.filter(completed=True)
    return render(request, 'CavQuest_app/task_list.html',
                  {'pending_tasks': pending_tasks, 'completed_tasks': completed_tasks})

def change_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        profile_picture = request.FILES.get('profile_picture')

        if new_username:
            if User.objects.filter(username=new_username).exists():
                return JsonResponse({'username_taken': True})
            request.user.username = new_username

        if profile_picture:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.profile_picture.save(profile_picture.name, profile_picture, save=True)
            user_profile.save()
        request.user.save()
        return JsonResponse({'username_taken': False})

    return render(request, 'user_profile.html', {'form': form})

def upload_task_image(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskImageForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('congratulations_page', task_id=task.id)
    else:
        form = TaskImageForm()

    return render(request, 'submission_details.html', {'form': form})