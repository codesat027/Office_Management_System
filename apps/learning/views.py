from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Lesson, CourseProgress
from .models import LessonProgress


def course_list(request):
    courses = Course.objects.all()

    total_courses = courses.count()
    completed_courses = 0
    in_progress_courses = 0
    progress_map = {}

    if request.user.is_authenticated:
        progress_records = CourseProgress.objects.filter(user=request.user)

        for record in progress_records:
            progress_map[record.course_id] = record.progress

            if record.progress >= 100:
                completed_courses += 1
            elif record.progress > 0:
                in_progress_courses += 1

    context = {
        'courses': courses,
        'total_courses': total_courses,
        'completed_courses': completed_courses,
        'in_progress_courses': in_progress_courses,
        'progress_map': progress_map,
    }

    return render(request, 'learning/course_list.html', context)

def course_detail(request, id):
    course = Course.objects.get(id=id)
    lessons = Lesson.objects.filter(course=course)

    lesson_id = request.GET.get('lesson')
    if lesson_id:
        selected_lesson = Lesson.objects.get(id=lesson_id)
    else:
        selected_lesson = lessons.first()

    completed_lessons = []
    if request.user.is_authenticated:
        completed_lessons = LessonProgress.objects.filter(
            user=request.user,
            lesson__course=course,
            is_completed=True
        ).values_list('lesson_id', flat=True)

    return render(request, 'learning/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'selected_lesson': selected_lesson,
        'completed_lessons': completed_lessons,
    })


@login_required
def mark_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    obj, created = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )

    obj.is_completed = True
    obj.save()

    return redirect(f'/learning/{lesson.course.id}/?lesson={lesson.id}')

@login_required
def add_course(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        Course.objects.create(
            title=title,
            description=description,
            image=image
        )

        return redirect('course_list')

    return render(request, 'learning/add_course.html')