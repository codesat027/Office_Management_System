import mimetypes
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Employee


@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/list.html', {'employees': employees})


@login_required
def add_employee(request):
    if request.method == "POST":
        Employee.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            department=request.POST.get('department'),
            position=request.POST.get('position')
        )
        return redirect('employee_list')

    return render(request, 'employees/add.html')


@login_required
def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":
        employee.name = request.POST.get('name')
        employee.email = request.POST.get('email')
        employee.department = request.POST.get('department')
        employee.position = request.POST.get('position')
        employee.save()
        return redirect('employee_list')

    return render(request, 'employees/edit.html', {'employee': employee})


@login_required
def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('employee_list')


@login_required
def profile_view(request):
    employee = Employee.objects.filter(user=request.user).first()

    return render(request, 'employees/profile.html', {
        'employee': employee,
        'display_email': employee.email if employee else request.user.email,
        'attendance': [],
        'tasks': [],
        'documents': [],
        'selected_document': None,
    })


@login_required
def upload_document(request):
    return render(request, 'employees/upload_document.html')


@login_required
def delete_document(request, id):
    return redirect('profile_view')


@login_required
def view_document(request, id):
    return redirect('profile_view')