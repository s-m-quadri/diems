from django.shortcuts import render, get_object_or_404
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import *
from home.views import render_form_generic
from codeshine.models import Assignment, Submission, Comment
from departments.models import Page


def specific_assignment(request, page_code, assignment_code):
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return render(request, "home/401.html", status=401)

    page = get_object_or_404(Page, Code=page_code)

    # Ensure user is in same department
    if not request.user.Department == page.Department:
        return render(request, "home/403.html", status=403)

    assignment = get_object_or_404(Assignment, pk=assignment_code)    
    my_submissions = Submission.objects.filter(In=assignment, By=request.user)
    all_submissions = Submission.objects.filter(In=assignment)

    class PostSubmissionForm(forms.Form):
        fieldAssignment = forms.CharField(
            label="Solution",
            widget=forms.Textarea,
            required=False,
            initial=assignment.GettingStarted_Template)

    max_marks = 0
    comments = []
    for submission in my_submissions:
        comments += [x for x in Comment.objects.filter(In=submission)]
        max_marks = max(submission.Points, max_marks)

    return render(request, "codeshine/index.html", {
        "title": f"Assignment - {assignment.Title}",
        "assignment": assignment,
        "submissions": my_submissions,
        "comments": comments,
        "all_submissions": all_submissions,
        "page_code": page_code,
        "assignment_code": assignment_code,
        "form": PostSubmissionForm(),
        "max_marks": max_marks,
    })


def post_assignment(request, page_code):
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return render(request, "home/401.html", status=401)

    page = get_object_or_404(Page, Code=page_code)

    # Ensure user is in same department
    if not request.user.Department == page.Department:
        return render(request, "home/403.html", status=403)

    # Ensure user is teacher
    if not request.user.is_teacher:
        return render(request, "home/403.html", status=403)

    return_url = reverse("departments:specific_department", kwargs={
        "code": page.Department.Code
    })

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
        comment_choices = (("Yes", "Yes! let student comment on results/submissions"),
                           ("No", "No! results/submission are fixed, no grievance."))
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
            In=page,
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

    return HttpResponseRedirect(return_url)


def submissions(request, page_code, assignment_code):
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return render(request, "home/401.html", status=401)

    page = get_object_or_404(Page, Code=page_code)

    # Ensure user is in same department
    if not request.user.Department == page.Department:
        return render(request, "home/403.html", status=403)

    assignment = get_object_or_404(Assignment, pk=assignment_code)
    submissions = Submission.objects.filter(In=assignment)

    # Ensure user is teacher or is allowed by students
    if not request.user.is_teacher:
        return render(request, "home/403.html", status=403)

    submission_users = []
    all_submissions = []
    for submission in submissions:
        if submission.By not in submission_users:
            submission_users += [submission.By]
            all_submissions += [(submission.By,
                                 [x for x in submissions.filter(By=submission.By)])]

    return render(request, "codeshine/submissions.html", {
        "title": f"{assignment.Title}",
        "page_code": page_code,
        "assignment_code": assignment_code,
        "assignment": assignment,
        "submission_users": submission_users,
        "all_submissions": all_submissions,
    })


def specific_submission(request, page_code, assignment_code, submission_code):
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return render(request, "home/401.html", status=401)

    page = get_object_or_404(Page, Code=page_code)

    # Ensure user is in same department
    if not request.user.Department == page.Department:
        return render(request, "home/403.html", status=403)

    assignment = get_object_or_404(Assignment, pk=assignment_code)
    submission = get_object_or_404(Submission, pk=submission_code)

    # Ensure user is teacher or the submission is of student them-self
    if not (request.user.is_teacher or request.user == submission.By):
        return render(request, "home/403.html", status=403)

    comments = [x for x in Comment.objects.filter(In=submission)]

    class PostEvaluationForm(forms.Form):
        fieldSubmissionPoints = forms.IntegerField(
            label="Evaluation Points",
            min_value=1,
            max_value=assignment.max_points,
            initial=submission.Points,
            required=True)
        fieldRemark = forms.CharField(
            label="Remark", max_length=1024, required=False,
            initial=submission.Remark)
        ideal_choices = (("No", "Maybe! but not suitable for sharing with others at result declaration"),
                         ("Yes", "Yes! and should be shared to all at result declaration"))
        fieldIdeal = forms.ChoiceField(
            label="Is ideal", initial="No", required=True, choices=ideal_choices)

    class PostCommentForm(forms.Form):
        fieldCommentTheme = forms.CharField(
            label="Theme", max_length=128, required=False)
        fieldComment = forms.CharField(
            label="Comment", widget=forms.Textarea, required=True)

    return render(request, "codeshine/submission.html", {
        "title": f"Submission #{submission.pk}",
        "page_code": page_code,
        "assignment_code": assignment_code,
        "submission_code": submission_code,
        "assignment": assignment,
        "submission": submission,
        "comments": comments,
        "form_evaluate": PostEvaluationForm(),
        "form_comment": PostCommentForm()
    })


def post_submission(request, page_code, assignment_code):
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return render(request, "home/401.html", status=401)

    page = get_object_or_404(Page, Code=page_code)

    # Ensure user is in same department
    if not request.user.Department == page.Department:
        return render(request, "home/403.html", status=403)

    assignment = get_object_or_404(Assignment, pk=assignment_code)

    # Ensure user is teacher or is allowed by students
    if not (request.user.is_teacher or assignment.open_for_submission):
        return render(request, "home/405.html", status=405)

    return_url = reverse("codeshine:assignments", kwargs={
        "page_code": page_code,
        "assignment_code": assignment_code
    })

    class PostSubmissionForm(forms.Form):
        fieldAssignment = forms.CharField(
            label="Solution", widget=forms.Textarea, required=False, initial=assignment.GettingStarted_Template)

    # If access via GET method
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
            In=assignment,
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


def post_evaluation(request, page_code, assignment_code, submission_code):
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return render(request, "home/401.html", status=401)

    page = get_object_or_404(Page, Code=page_code)
    
    # Ensure user is in same department
    if not request.user.Department == page.Department:
        return render(request, "home/403.html", status=403)

    # Ensure user is logged in as teacher
    if not request.user.is_teacher:
        return render(request, "home/403.html", status=403)

    return_url = reverse("codeshine:submission", kwargs={
        "page_code": page_code,
        "assignment_code": assignment_code,
        "submission_code": submission_code
    })

    # If access via GET method
    if not request.method == "POST":
        return HttpResponseRedirect(return_url)

    assignment = Assignment.objects.get(pk=assignment_code)
    submission = Submission.objects.get(pk=submission_code)

    class PostEvaluationForm(forms.Form):
        fieldSubmissionPoints = forms.IntegerField(
            label="Evaluation Points",
            min_value=1,
            max_value=assignment.max_points,
            initial=submission.Points,
            required=True)
        fieldRemark = forms.CharField(
            label="Remark", max_length=1024, required=False,
            initial=submission.Remark)

        ideal_choices = (("No", "Maybe! but not suitable for sharing with others at result declaration"),
                         ("Yes", "Yes! and should be shared to all at result declaration"))
        fieldIdeal = forms.ChoiceField(
            label="Is ideal", initial="No", required=True, choices=ideal_choices)

    raw_form = PostEvaluationForm(request.POST)

    if not raw_form.is_valid():
        return render(request, "home/400.html", context={
            "return_url": return_url,
            "backup_data": PostEvaluationForm(request.POST)
        })

    try:
        # Gather Requirements
        assignment = Assignment.objects.get(pk=assignment_code)
        submission = Submission.objects.get(pk=submission_code)

        # Critical Section
        form_data = raw_form.cleaned_data
        new_evaluation = submission
        new_evaluation.Points = form_data["fieldSubmissionPoints"]
        new_evaluation.Remark = form_data["fieldRemark"]
        new_evaluation.is_ideal = False if form_data["fieldIdeal"] != "Yes" else True
        new_evaluation.save()

        # Auto Review Generation
        auto_comment_content = f"""You have been awarded with {form_data["fieldSubmissionPoints"]} / {assignment.max_points}. As per assignment the passing marks is {assignment.passing_points} / {assignment.max_points}. The marks/points are meant for analysis purpose only, and no significance to define the value of a human being. Failure/Success are the part of your life, never let them to dominate your mindset. Remark by teacher "{form_data["fieldRemark"]}"."""
        new_comment = Comment(
            By=request.user,
            In=submission,
            Comment=auto_comment_content,
        )
        new_comment.save()
    except Exception as exception:
        return render(request, "home/400.html", context={
            "exception": exception,
            "return_url": return_url,
            "backup_data": PostEvaluationForm(request.POST)
        })

    return HttpResponseRedirect(return_url)


def post_comment(request, page_code, assignment_code, submission_code):
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return render(request, "home/401.html", status=401)

    # Ensure user is in same department
    if not request.user.Department == Page.objects.get(Code=page_code).Department:
        return render(request, "home/403.html", status=403)

    assignment = Assignment.objects.get(pk=assignment_code)
    submission = Submission.objects.get(pk=submission_code)

    # Ensure user is teacher or is allowed by students
    if not (request.user.is_teacher or assignment.open_for_comment):
        return render(request, "home/405.html", status=405)

    return_url = reverse("codeshine:submission", kwargs={
        "page_code": page_code,
        "assignment_code": assignment_code,
        "submission_code": submission_code
    })

    class PostCommentForm(forms.Form):
        fieldCommentTheme = forms.CharField(
            label="Theme", max_length=128, required=False)
        fieldComment = forms.CharField(
            label="Comment", widget=forms.Textarea, required=True)

    if not request.method == "POST":
        return HttpResponseRedirect(return_url)

    raw_form = PostCommentForm(request.POST)
    if not raw_form.is_valid():
        return render(request, "home/400.html", context={
            "return_url": return_url,
            "backup_data": PostCommentForm(request.POST)
        })

    try:
        # Critical Section
        form_data = raw_form.cleaned_data
        new_comment = Comment(
            By=request.user,
            In=submission,
            Theme=form_data["fieldCommentTheme"],
            Comment=form_data["fieldComment"],
        )
        new_comment.save()

    except Exception as exception:
        return render(request, "home/400.html", context={
            "exception": exception,
            "return_url": return_url,
            "backup_data": PostCommentForm(request.POST)
        })

    return HttpResponseRedirect(return_url)
