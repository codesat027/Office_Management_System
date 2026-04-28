from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.employees.models import Employee
from .models import Task


# @login_required
# def task_list(request):
#     tasks = Task.objects.all().order_by('-id')
#     employees = Employee.objects.all()

#     return render(request, 'tasks/list.html', {
#         'tasks': tasks,
#         'employees': employees
#     })

def task_list(request):
    tasks = Task.objects.all().order_by('-id')

    status = request.GET.get('status')
    priority = request.GET.get('priority')

    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    pending_count = tasks.filter(status='Pending').count()
    progress_count = tasks.filter(status='In Progress').count()
    completed_count = tasks.filter(status='Completed').count()

    return render(request, 'tasks/list.html', {
        'tasks': tasks,
        'pending_count': pending_count,
        'progress_count': progress_count,
        'completed_count': completed_count,
    })



@login_required
def add_task(request):
    employees = Employee.objects.all()

    if request.method == "POST":
        employee_id = request.POST.get('employee')
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')

        employee = get_object_or_404(Employee, id=employee_id)

        Task.objects.create(
            employee=employee,
            title=title,
            description=description,
            status=status
        )

        return redirect('task_list')

    return render(request, 'tasks/add.html', {
        'employees': employees
    })


@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id)
    employees = Employee.objects.all()

    if request.method == "POST":
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status')

        employee_id = request.POST.get('employee')
        task.employee = get_object_or_404(Employee, id=employee_id)

        task.save()
        return redirect('task_list')

    return render(request, 'tasks/edit.html', {
        'task': task,
        'employees': employees
    })


@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    return redirect('task_list')