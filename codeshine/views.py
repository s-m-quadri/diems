from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import *
from home.views import render_form_generic
from codeshine.models import Assignment, Submission, Comment
from departments.models import Page


def index(request, page_code):
    return render(request, "codeshine/index.html", {
        "massage": "This is codeshine route"
    })

def assignment_index(request, page_code, assignment_code):
    assignment = Assignment.objects.get(pk=assignment_code)
    return render(request, "codeshine/index.html", {
        "title": f"Assignment - {Assignment.objects.get(pk=assignment_code).Title}",
        "assignment": assignment,
        "submissions": Submission.objects.filter(In=assignment, By=request.user),
    })

def post_assignment(request, page_code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("departments:index", kwargs={"code": Page.objects.get(Code=page_code).Department.Code}))

    class PostAssignmentForm(forms.Form):
        fieldTitle = forms.CharField(
            label="Title", max_length=128, required=True, strip=True)
        fieldDescription = forms.CharField(
            label="Description", max_length=1024, required=False, strip=True)
        fieldMaxPoints = forms.IntegerField(
            label="Maximum Possible Points", min_value=0, initial=100, required=True)
        fieldPassingPoints = forms.IntegerField(
            label="Satisfactory Passing Points", min_value=0, initial=35, required=True)
        submission_choices = (("Yes", "Yes! Allow students to make submissions"),
                              ("No", "No! Close the submission feature for students"))
        fieldOpenForSubmission = forms.ChoiceField(
            label="Allow Submissions", required=True, choices=submission_choices)
        comment_choices = (("Yes", "Yes! let student comment"),
                           ("No", "No! Don't take any comments"))
        fieldOpenForComment = forms.ChoiceField(
            label="Allow Comments", required=True, choices=comment_choices)
        fieldInstructions = forms.CharField(
            label="Instructions", widget=forms.Textarea, required=False)
        fieldGettingStarted = forms.CharField(
            label="Getting Started Template", widget=forms.Textarea, required=False)

    form_title = "Create Assignment"
    form_to = reverse("codeshine:post", kwargs={"page_code": page_code})
    form_action = "Post Assignment"

    if not request.method == "POST":
        return render_form_generic(
            request, form_title, form_to, form_action, PostAssignmentForm())

    raw_form = PostAssignmentForm(request.POST)
    if not raw_form.is_valid():
        return render_form_generic(
            request, form_title, form_to, form_action, PostAssignmentForm(request.POST))

    try:
        form_data = raw_form.cleaned_data

        new_assignment = Assignment(
            By=request.user,
            In=Page.objects.get(Code=page_code),
            Title=form_data["fieldTitle"],
            Description=form_data["fieldDescription"],
            Instructions=form_data["fieldInstructions"],
            GettingStarted_Template=form_data["fieldGettingStarted"],
            max_points=form_data["fieldMaxPoints"],
            passing_points=form_data["fieldPassingPoints"]
        )

        if form_data["fieldOpenForSubmission"] == "Yes":
            new_assignment.open_for_submission = True
        else:
            new_assignment.open_for_submission = False

        if form_data["fieldOpenForComment"] == "Yes":
            new_assignment.open_for_comment = True
        else:
            new_assignment.open_for_comment = False

        new_assignment.save()

    except Exception as massage:
        return render_form_generic(
            request, form_title, form_to, form_action,
            PostAssignmentForm(request.POST),
            "Something went wrong, please contact support team regarding exception '{}'".format(massage))

    return HttpResponseRedirect(reverse("departments:index", kwargs={"code": Page.objects.get(Code=page_code).Department.Code}))


def post_submission(request, page_code, assignment_code):
    if not request.user.is_teacher:
        return HttpResponseRedirect(reverse("departments:index", kwargs={"code": Page.objects.get(Code=page_code).Department.Code}))

    class PostSubmissionForm(forms.Form):
        fieldAssignment = forms.CharField(
            label="Solution", widget=forms.Textarea, required=False, initial=Assignment.objects.get(pk=assignment_code).GettingStarted_Template)

    form_title = "Submit Assignment"
    form_to = reverse("codeshine:submit", kwargs={
                      "page_code": page_code, "assignment_code": assignment_code})
    form_action = "Submit This Solution"

    if not request.method == "POST":
        return render_form_generic(
            request, form_title, form_to, form_action, PostSubmissionForm())

    raw_form = PostSubmissionForm(request.POST)
    if not raw_form.is_valid():
        return render_form_generic(
            request, form_title, form_to, form_action, PostSubmissionForm(request.POST))

    try:
        form_data = raw_form.cleaned_data

        new_submission = Submission(
            By=request.user,
            In=Assignment.objects.get(pk=assignment_code),
            Assignment=form_data["fieldAssignment"]
        )
        new_submission.save()

    except Exception as massage:
        return render_form_generic(
            request, form_title, form_to, form_action,
            PostSubmissionForm(request.POST),
            "Something went wrong, please contact support team regarding exception '{}'".format(massage))

    return HttpResponseRedirect(reverse("departments:index", kwargs={"code": Page.objects.get(Code=page_code).Department.Code}))
