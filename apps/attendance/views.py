from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.employees.models import Employee
from .models import Attendance, Leave, AdditionalLeave
from django.db.models import Sum, F, ExpressionWrapper, IntegerField
from django.db.models.functions import ExtractMonth, ExtractYear
from django.utils import timezone
import calendar


@login_required
def attendance_list(request):
    records = Attendance.objects.all().order_by('-date')
    employees = Employee.objects.all()
    employee_id = request.GET.get('employee')
    date = request.GET.get('date')

    # Filtering logic
    if employee_id:
        records = records.filter(employee_id=employee_id)
    if date:
        records = records.filter(date=date)

    # --- TODAY'S STATS LOGIC ---
    today = timezone.now().date()
    today_attendance = Attendance.objects.filter(date=today)
    
    total_employees = employees.count()
    present_today = today_attendance.filter(status='Present').count()
    absent_today = today_attendance.filter(status='Absent').count()
    late_today = today_attendance.filter(status='Late').count()

    return render(request, 'attendance/list.html', {
        'records': records,
        'employees': employees,
        'selected_employee': employee_id,
        'selected_date': date,
        # Stats context
        'total_employees': total_employees,
        'present_count': present_today,
        'absent_count': absent_today,
        'late_count': late_today,
    })

# ... baaki functions (add_attendance, leave_list, etc.) same rahenge jo aapne diye hain ...

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
    # Dono type ki leaves ko fetch karke template mein bhejna
    leaves = Leave.objects.all().order_by('-id')
    additional_leaves = AdditionalLeave.objects.all().order_by('-id')
    employees = Employee.objects.all()
    return render(request, 'attendance/leave_list.html', {
        'leaves': leaves,
        'additional_leaves': additional_leaves,
        'employees': employees,
    })

@login_required
def add_leave(request):
    if request.method == "POST":
        Leave.objects.create(
            employee_id=request.POST.get('employee'),
            leave_type=request.POST.get('leave_type'),
            start_date=request.POST.get('from_date'),
            end_date=request.POST.get('to_date'),
            reason=request.POST.get('reason'),
            status='Pending'
        )
        return redirect('leave_list')
    employees = Employee.objects.all()
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

# --- ADDITIONAL LEAVE ACTIONS ---
@login_required
def approve_additional_leave(request, id):
    leave = get_object_or_404(AdditionalLeave, id=id)
    leave.status = 'Approved'
    leave.save()
    return redirect('leave_list')

@login_required
def reject_additional_leave(request, id):
    leave = get_object_or_404(AdditionalLeave, id=id)
    leave.status = 'Rejected'
    leave.save()
    return redirect('leave_list')

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
        # Ab ye submit hote hi Leave History page par bhejega
        return redirect('leave_list')
    return redirect('leave_balance')


@login_required
def leave_balance(request):
    employees = Employee.objects.all()
    employee_id = request.GET.get('employee')

    if not employee_id and employees.exists():
        employee_id = employees.first().id

    selected_employee = None
    approved_leaves = Leave.objects.none()
    additional_leaves_list = AdditionalLeave.objects.none()
    total_leaves = 10
    leaves_taken = 0
    leaves_remaining = 0
    additional_leaves_count = 0

    if employee_id:
        selected_employee = get_object_or_404(Employee, id=employee_id)
        total_leaves = selected_employee.leave_balance or 0
        approved_leaves = Leave.objects.filter(employee=selected_employee, status='Approved').order_by('-id')
        additional_leaves_list = AdditionalLeave.objects.filter(employee=selected_employee, status='Approved').order_by('-id')

        normal_days = sum(leave.total_days for leave in approved_leaves)
        additional_days = sum(leave.total_days for leave in additional_leaves_list)

        leaves_taken = normal_days
        leaves_remaining = max(total_leaves - normal_days, 0)
        additional_leaves_count = max(normal_days - total_leaves, 0) + additional_days

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
def leave_report(request):
    # Base Query
    leaves = Leave.objects.all().order_by('-start_date')
    employees = Employee.objects.all()
    
    employee_id = request.GET.get('employee')
    year = request.GET.get('year')

    if employee_id:
        leaves = leaves.filter(employee_id=employee_id)
    if year:
        leaves = leaves.filter(start_date__year=year)

    # selected_year set karein
    selected_year = int(year) if year else 2026

    # FIX: total_days ko database level par calculate karna (end_date - start_date + 1)
    monthly_data = (
        leaves.filter(start_date__year=selected_year, status='Approved')
        .annotate(month=ExtractMonth('start_date'))
        .annotate(
            duration=ExpressionWrapper(
                F('end_date') - F('start_date'), 
                output_field=IntegerField()
            )
        )
        .values('month')
        # Duration seconds ya days mein hoti hai, isliye hum use extract karke Sum karenge
        .annotate(total_days_count=Sum(F('duration') / (1000000 * 60 * 60 * 24)) + Sum(1)) 
        .order_by('month')
    )

    # Simplest way for Chart Data if annotate is tricky with durations:
    month_names = [calendar.month_name[i] for i in range(1, 13)]
    monthly_leave_days = [0] * 12
    
    # Chart ke liye calculation
    for leave in leaves.filter(start_date__year=selected_year, status='Approved'):
        m = leave.start_date.month
        monthly_leave_days[m-1] += leave.total_days # Property yahan loop mein kaam karegi

    # Get unique years
    years = Leave.objects.dates('start_date', 'year', order='DESC')
    year_list = [y.year for y in years]

    return render(request, 'attendance/leave_report.html', {
        'leaves': leaves,
        'employees': employees,
        'years': year_list,
        'selected_employee': employee_id,
        'selected_year': selected_year,
        'month_names': month_names,
        'monthly_leave_days': monthly_leave_days,
    })