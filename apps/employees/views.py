import mimetypes
from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Employee, Document
from apps.attendance.models import Attendance
from apps.tasks.models import Task

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
            phone=request.POST.get('phone'),
            department=request.POST.get('department'),
            position=request.POST.get('position'),
        )
        return redirect('employee_list')
    return render(request, 'employees/add.html')

@login_required
def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == "POST":
        employee.name = request.POST.get('name')
        employee.email = request.POST.get('email')
        employee.phone = request.POST.get('phone')
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
    # Try to get the employee linked to the logged-in user
    employee = Employee.objects.filter(user=request.user).first()
    
    # Handle Profile Update
    if request.method == "POST":
        if employee:
            employee.name = request.POST.get('name', employee.name)
            employee.phone = request.POST.get('phone')
            employee.department = request.POST.get('department')
            employee.position = request.POST.get('position')
            employee.about_me = request.POST.get('about_me')
            
            if request.FILES.get('photo'):
                employee.photo = request.FILES.get('photo')
            
            employee.save()
            return redirect('profile_view')

    display_email = employee.email if employee and employee.email else request.user.email
    attendance = Attendance.objects.filter(employee=employee).order_by('-date') if employee else []
    tasks = Task.objects.filter(employee=employee).order_by('-id') if employee else []
    documents = Document.objects.filter(employee=employee).order_by('-uploaded_at') if employee else []

    selected_document = None
    doc_id = request.GET.get('doc')
    if doc_id and employee:
        selected_document = Document.objects.filter(id=doc_id, employee=employee).first()

    return render(request, 'employees/profile.html', {
        'employee': employee,
        'display_email': display_email,
        'attendance': attendance,
        'tasks': tasks,
        'documents': documents,
        'selected_document': selected_document,
    })

@login_required
def upload_document(request):
    employee = Employee.objects.filter(user=request.user).first()
    if request.method == "POST":
        title = request.POST.get('title')
        file = request.FILES.get('file')
        if employee and file:
            Document.objects.create(
                employee=employee,
                title=title,
                file=file
            )
        return redirect('profile_view')
    return render(request, 'employees/upload_document.html')

@login_required
def delete_document(request, id):
    # Ensure user can only delete their own documents or is admin
    document = get_object_or_404(Document, id=id)
    document.delete()
    return redirect('profile_view')

@login_required
def view_document(request, id):
    document = get_object_or_404(Document, id=id)
    file_path = document.file.path
    content_type, _ = mimetypes.guess_type(file_path)
    if not content_type:
        content_type = 'application/octet-stream'
    
    response = FileResponse(document.file.open('rb'), content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{document.file.name}"'
    return response