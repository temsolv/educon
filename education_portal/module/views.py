from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden

from module.forms import NewModuleForm
from module.models import Module
from classroom.models import Course


def new_module(request, course_id):
    if request.user.profile.role.name != 'admin' and request.user.is_staff == False:
        return redirect("index")

    user = request.user
    course = get_object_or_404(Course, id=course_id)

    if user != course.user:
        return HttpResponseForbidden()
    else:
        if request.method == "POST":
            form = NewModuleForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get("title")
                m = Module.objects.create(title=title, user=user)
                course.modules.add(m)
                course.save()
                return redirect("modules", course_id=course_id)
        else:
            form = NewModuleForm()

    context = {
        "form": form,
    }

    return render(request, "module/newmodule.html", context)


def course_modules(request, course_id):
    user = request.user
    course = get_object_or_404(Course, id=course_id)

    teacher_mode = False
    if user == course.user:
        teacher_mode = True

    context = {
        "teacher_mode": teacher_mode,
        "course": course,
    }
    return render(request, "module/modules.html", context)
