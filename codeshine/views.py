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


def assignment_index(request, page_code, assignment_code, error=None, warning=None, message=None):
    class PostSubmissionForm(forms.Form):
        fieldAssignment = forms.CharField(
            label="Solution",
            widget=forms.Textarea,
            required=False,
            initial=Assignment.objects.get(pk=assignment_code).GettingStarted_Template)

    assignment = Assignment.objects.get(pk=assignment_code)
    my_submissions = Submission.objects.filter(In=assignment, By=request.user)
    all_submissions = Submission.objects.filter(In=assignment)
    comments = []
    for submission in my_submissions:
        comments += [x for x in Comment.objects.filter(In=submission)]

    return render(request, "codeshine/index.html", {
        "title": f"Assignment - {Assignment.objects.get(pk=assignment_code).Title}",
        "assignment": assignment,
        "submissions": my_submissions,
        "comments": comments,
        "all_submissions": all_submissions,
        "page_code": page_code,
        "assignment_code": assignment_code,
        "form": PostSubmissionForm(),
        "error": error,
        "warning": warning,
        "message": message,
    })


def post_assignment(request, page_code):
    if not request.user.is_teacher:
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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("accounts:login"))

    return_url = reverse("codeshine:assignments", kwargs={
        "page_code": page_code,
        "assignment_code": assignment_code
    })

    class PostSubmissionForm(forms.Form):
        fieldAssignment = forms.CharField(
            label="Solution", widget=forms.Textarea, required=False, initial=Assignment.objects.get(pk=assignment_code).GettingStarted_Template)

    if not request.method == "POST":
        return HttpResponseRedirect(return_url)

    raw_form = PostSubmissionForm(request.POST)
    if not raw_form.is_valid():
        return render(request, "home/400.html", context={
            "return_url": return_url,
            "backup_data": PostSubmissionForm(request.POST)
        })

    try:
        # Critical Section
        form_data = raw_form.cleaned_data
        new_submission = Submission(
            By=request.user,
            In=Assignment.objects.get(pk=assignment_code),
            Assignment=form_data["fieldAssignment"]
        )
        new_submission.save()

    except Exception as exception:
        return render(request, "home/400.html", context={
            "exception": exception,
            "return_url": return_url,
            "backup_data": PostSubmissionForm(request.POST)
        })

    return HttpResponseRedirect(return_url)


def submissions(request, page_code, assignment_code):
    assignment = Assignment.objects.get(pk=assignment_code)
    submissions = Submission.objects.filter(In=assignment)
    submission_users = []
    all_submissions = []
    for submission in submissions:
        if submission.By not in submission_users:
            submission_users += [submission.By]
            all_submissions += [(submission.By,
                                 [x for x in submissions.filter(By=submission.By)])]

    return render(request, "codeshine/submissions.html", {
        "title": f"Submissions - {Assignment.objects.get(pk=assignment_code).Title}",
        "page_code": page_code,
        "assignment_code": assignment_code,
        "assignment": assignment,
        "submission_users": submission_users,
        "all_submissions": all_submissions,
    })


def submission_index(request, page_code, assignment_code, submission_code):
    assignment = Assignment.objects.get(pk=assignment_code)
    submission = Submission.objects.get(pk=submission_code)
    comments = [x for x in Comment.objects.filter(In=submission)]

    return render(request, "codeshine/submission.html", {
        "title": f"Submission #{submission.pk}",
        "page_code": page_code,
        "assignment_code": assignment_code,
        "submission_code": submission_code,
        "assignment": assignment,
        "submission": submission,
        "comments": comments
    })


def post_evaluation(request, page_code, assignment_code, submission_code):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("departments:index", kwargs={"code": Page.objects.get(Code=page_code).Department.Code}))

    class PostEvaluationForm(forms.Form):
        fieldSubmissionPoints = forms.IntegerField(
            label="Evaluation Points",
            min_value=1,
            max_value=Assignment.objects.get(pk=assignment_code).max_points,
            initial=Submission.objects.get(pk=submission_code).Points,
            required=True)
        fieldRemark = forms.CharField(
            label="Remark", max_length=1024, required=False,
            initial=Submission.objects.get(pk=submission_code).Remark)

        ideal_choices = (("No", "Maybe! but not suitable for sharing with others at result declaration"),
                         ("Yes", "Yes! and should be shared to all at result declaration"))
        fieldIdeal = forms.ChoiceField(
            label="Is ideal", initial="No", required=True, choices=ideal_choices)
        fieldComment = forms.CharField(
            label="Additional Comment", widget=forms.Textarea, required=False)
        fieldCommentTheme = forms.CharField(
            label="Additional Comment Theme", max_length=128, required=False)

    form_title = f"Evaluate {Submission.objects.get(pk=submission_code).By.username}'s Submission"
    form_to = reverse("codeshine:evaluate", kwargs={
                      "page_code": page_code,
                      "assignment_code": assignment_code,
                      "submission_code": submission_code})
    form_action = "Finalize this one"

    if not request.method == "POST":
        return render_form_generic(
            request, form_title, form_to, form_action, PostEvaluationForm())

    raw_form = PostEvaluationForm(request.POST)
    if not raw_form.is_valid():
        return render_form_generic(
            request, form_title, form_to, form_action, PostEvaluationForm(request.POST))

    try:
        form_data = raw_form.cleaned_data

        new_evaluation = Submission.objects.get(pk=submission_code)
        new_evaluation.Points = form_data["fieldSubmissionPoints"]
        new_evaluation.Remark = form_data["fieldRemark"]
        new_evaluation.is_ideal = False if form_data["fieldIdeal"] != "Yes" else True
        new_evaluation.save()

        if form_data["fieldCommentTheme"] or form_data["fieldComment"]:
            new_comment = Comment(
                By=request.user,
                In=Submission.objects.get(pk=submission_code),
                Theme=form_data["fieldCommentTheme"],
                Comment=form_data["fieldComment"],
            )
            new_comment.save()

    except Exception as massage:
        return render_form_generic(
            request, form_title, form_to, form_action,
            PostEvaluationForm(request.POST),
            "Something went wrong, please contact support team regarding exception '{}'".format(massage))

    return HttpResponseRedirect(reverse("codeshine:submission", kwargs={
        "page_code": page_code,
        "assignment_code": assignment_code,
        "submission_code": submission_code
    }))
