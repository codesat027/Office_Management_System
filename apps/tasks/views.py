from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.employees.models import Employee
from .models import Task

@login_required
def task_list(request):
    # Base Queryset
    all_tasks = Task.objects.all().select_related('employee', 'assigned_by').order_by('-id')
    
    # Filtering Logic
    status_query = request.GET.get('status')
    priority_query = request.GET.get('priority')

    tasks = all_tasks
    if status_query:
        tasks = tasks.filter(status=status_query)
    if priority_query:
        tasks = tasks.filter(priority=priority_query)

    # Counts for summary cards
    pending_count = all_tasks.filter(status='Pending').count()
    progress_count = all_tasks.filter(status='In Progress').count()
    completed_count = all_tasks.filter(status='Completed').count()

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
        status = request.POST.get('status', 'Pending')
        priority = request.POST.get('priority', 'Medium')
        deadline = request.POST.get('deadline')
        progress = request.POST.get('progress', 0)

        # Employee fetching
        employee = get_object_or_404(Employee, id=employee_id)

        # Task Creation with Assigned By (request.user)
        Task.objects.create(
            employee=employee,
            assigned_by=request.user,  # Saved the admin who created it
            title=title,
            description=description,
            status=status,
            priority=priority,
            deadline=deadline if deadline else None,
            progress=progress if progress else 0
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