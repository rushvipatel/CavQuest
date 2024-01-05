from django.test import TestCase
from django.urls import reverse
from .models import Task,Hint,Place, UserSubmission

# Resource(s) for testing: https://docs.djangoproject.com/en/4.2/topics/testing/tools/

class TaskModelTests(TestCase):
    def test_unapproved_task_is_not_displayed_in_task_list(self):
        unapproved_task = Task.objects.create(
            task_text = "unapproved task",
            approved_status=False
        )
        response = self.client.get(reverse("CavQuest_app:task_list"))
        self.assertNotContains(response, unapproved_task.task_text)

class UserSubmissionModelTests(TestCase):
    def test_approved_user_submission_not_shown_for_admin(self):
        approved_submission = UserSubmission.objects.create(
            task_text = "approved submission",
            approved = True
        )
        response = self.client.get(reverse("CavQuest_app:display_submissions"))
        self.assertNotContains(response, approved_submission.task_text)




