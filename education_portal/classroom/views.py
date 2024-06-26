from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from classroom.models import Course
from classroom.forms import NewCourseForm
from authy.models import Profile


@login_required
def index(request):
    return render(request, "index.html")


@login_required
def my_courses(request):
    if request.user.is_staff:
        return redirect("index")
    profile = Profile.objects.get(user=request.user)
    active_courses = set()
    completed_courses = set()
    expired_courses = set()

    for ac in profile.assigned_courses.all():
        if ac.is_completed == True:
            completed_courses.add(ac)
        if ac.is_completed == False and ac.is_expired == False:
            active_courses.add(ac)
        if ac.is_expired == True:
            expired_courses.add(ac.course)

    active_courses_list = list(active_courses)
    completed_courses_list = list(completed_courses)
    expired_courses_list = list(expired_courses)

    context = {
        "active_courses": active_courses_list,
        "completed_courses": completed_courses_list,
        "expired_courses": expired_courses_list,
    }

    return render(request, "classroom/courses.html", context)


@login_required
def new_course(request):
    if request.user.profile.role.name != 'admin' and request.user.is_staff == False:
        return redirect("index")

    user = request.user
    if request.method == "POST":
        form = NewCourseForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get("picture")
            title = form.cleaned_data.get("title")
            description = form.cleaned_data.get("description")
            syllabus = form.cleaned_data.get("syllabus")
            Course.objects.create(
                picture=picture,
                title=title,
                description=description,
                syllabus=syllabus,
                user=user,
            )
            return redirect("manage-courses")
    else:
        form = NewCourseForm()

    context = {
        "form": form,
    }

    return render(request, "classroom/newcourse.html", context)


@login_required
def course(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)
    teacher_mode = False

    if user == course.user:
        teacher_mode = True

    context = {
        "course": course,
        "teacher_mode": teacher_mode,
    }

    return render(request, "classroom/course.html", context)


@login_required
def delete_course(request, course_id):
    if request.user.profile.role.name != 'admin' and request.user.is_staff == False:
        return redirect("index")

    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponseForbidden()
    else:
        course.delete()

    return redirect("manage-courses")


@login_required
def manage_courses(request):
    if request.user.profile.role.name != 'admin' and request.user.is_staff == False:
        return redirect("index")

    user = request.user
    courses = Course.objects.filter(user=user)

    context = {
        "courses": courses,
    }

    return render(request, "classroom/mycourses.html", context)
