from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.employees.models import Employee
from .models import Attendance, Leave, AdditionalLeave

def attendance_list(request):
    records = Attendance.objects.all()

    total_records = records.count()
    present_count = records.filter(status='Present').count()
    absent_count = records.filter(status='Absent').count()
    late_count = records.filter(status='Late').count()

    return render(request, 'attendance/list.html', {
        'records': records,
        'total_records': total_records,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
    })


@login_required
def add_attendance(request):
    employees = Employee.objects.all()

    if request.method == "POST":
        Attendance.objects.create(
            employee_id=request.POST.get('employee'),
            date=request.POST.get('date'),
            status=request.POST.get('status')
        )
        return redirect('attendance_list')

    return render(request, 'attendance/add.html', {'employees': employees})


@login_required
def leave_list(request):
    leaves = Leave.objects.all().order_by('-id')
    employees = Employee.objects.all()

    if request.method == "POST":
        Leave.objects.create(
    employee_id=request.POST.get('employee'),
    leave_type=request.POST.get('leave_type'),   # ✅ ADD THIS
    start_date=request.POST.get('from_date'),
    end_date=request.POST.get('to_date'),
    reason=request.POST.get('reason'),
    status='Pending'
)
        return redirect('leave_list')

    return render(request, 'attendance/leave_list.html', {
        'leaves': leaves,
        'employees': employees,
    })


@login_required
def add_leave(request):
    employees = Employee.objects.all()

    if request.method == "POST":
        Leave.objects.create(
    employee_id=request.POST.get('employee'),
    leave_type=request.POST.get('leave_type'),   # ✅ ADD THIS
    start_date=request.POST.get('from_date'),
    end_date=request.POST.get('to_date'),
    reason=request.POST.get('reason'),
    status='Pending'
)
        return redirect('leave_list')

    return render(request, 'attendance/add_leave.html', {'employees': employees})


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
def leave_report(request):
    leaves = Leave.objects.all().order_by('-id')
    return render(request, 'attendance/leave_report.html', {'leaves': leaves})

@login_required
def leave_balance(request):
    employees = Employee.objects.all()

    employee_id = request.GET.get('employee')

    # 👉 DEFAULT: first employee auto select
    if not employee_id and employees.exists():
        employee_id = employees.first().id

    selected_employee = None
    approved_leaves = Leave.objects.none()
    additional_leaves_list = AdditionalLeave.objects.none()

    total_leaves = 10
    leaves_taken = 0
    additional_leaves_count = 0
    leaves_remaining = 0

    if employee_id:
        selected_employee = get_object_or_404(Employee, id=employee_id)

        total_leaves = selected_employee.leave_balance or 0

        approved_leaves = Leave.objects.filter(
            employee=selected_employee,
            status='Approved'
        )

        additional_leaves_list = AdditionalLeave.objects.filter(
            employee=selected_employee,
            status='Approved'
        )

        # ✅ main leaves
normal_days = sum(l.total_days for l in approved_leaves)
additional_days = sum(l.total_days for l in additional_leaves_list)

# ✅ only normal leaves count
leaves_taken = normal_days

# ✅ extra leaves only
additional_leaves_count = max(normal_days - total_leaves, 0) + additional_days

          # ✅ remaining only from quota
leaves_remaining = max(total_leaves - normal_days, 0)

return render(request, 'attendance/leave_balance.html', {
        'employees': employees,
        'selected_employee': selected_employee,
        'approved_leaves': approved_leaves,
        'additional_leaves_list': additional_leaves_list,
        'total_leaves': total_leaves,
        'leaves_taken': leaves_taken,
        'leaves_remaining': leaves_remaining,
        'additional_leaves_count': additional_leaves_count,
    })

@login_required
def add_additional_leave(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee')

        AdditionalLeave.objects.create(
            employee_id=employee_id,
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            reason=request.POST.get('reason'),
            status='Pending'
        )

        # 👉 same employee page pe redirect karega
        return redirect(f'/attendance/leave/balance/?employee={employee_id}')

    return redirect('leave_balance')