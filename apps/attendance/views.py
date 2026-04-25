from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.employees.models import Employee
from .models import Attendance, Leave


@login_required
def attendance_list(request):
    records = Attendance.objects.all().order_by('-date')

    total_records = records.count()
    present_count = records.filter(status='Present').count()
    absent_count = records.filter(status='Absent').count()
    late_count = records.filter(status='Late').count()

    employees = Employee.objects.all()

    return render(request, 'attendance/list.html', {
        'records': records,
        'employees': employees,
        'total_records': total_records,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
    })


@login_required
def add_attendance(request):
    employees = Employee.objects.all()

    if request.method == "POST":
        employee_id = request.POST.get('employee')
        date = request.POST.get('date')
        status = request.POST.get('status')

        employee = get_object_or_404(Employee, id=employee_id)

        Attendance.objects.create(
            employee=employee,
            date=date,
            status=status
        )

        return redirect('attendance_list')

    return render(request, 'attendance/add.html', {
        'employees': employees
    })


@login_required
def leave_list(request):
    leaves = Leave.objects.all().order_by('-id')
    employees = Employee.objects.all()

    return render(request, 'attendance/leave.html', {
        'leaves': leaves,
        'employees': employees
    })


@login_required
def add_leave(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee')
        reason = request.POST.get('reason')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        employee = get_object_or_404(Employee, id=employee_id)

        Leave.objects.create(
            employee=employee,
            reason=reason,
            start_date=start_date,
            end_date=end_date,
            status='Pending'
        )

        return redirect('leave_list')

    employees = Employee.objects.all()
    return render(request, 'attendance/add_leave.html', {
        'employees': employees
    })


@login_required
def approve_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.status = 'Approved'
    leave.save()
    return redirect('leave_list')


@login_required
def reject_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.status = 'Rejected'
    leave.save()
    return redirect('leave_list')


@login_required
def leave_balance(request):
    employees = Employee.objects.all()
    return render(request, 'attendance/leave_balance.html', {
        'employees': employees
    })

@login_required
def leave_report(request):
    leaves = Leave.objects.all().order_by('-id')
    return render(request, 'attendance/leave_report.html', {
        'leaves': leaves
    })