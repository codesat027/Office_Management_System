from django.shortcuts import render, redirect
from .models import Expense
from apps.employees.models import Employee


# def expense_list(request):
#     expenses = Expense.objects.all()
#     employees = Employee.objects.all()

#     receipt_expense = None
#     receipt_id = request.GET.get('receipt')

#     if receipt_id:
#         try:
#             receipt_expense = Expense.objects.get(id=receipt_id)
#         except Expense.DoesNotExist:
#             receipt_expense = None

#     return render(request, 'expenses/list.html', {
#         'expenses': expenses,
#         'employees': employees,
#         'receipt_expense': receipt_expense,
#     })

def expense_list(request):
    all_expenses = Expense.objects.all().order_by('-id')
    employees = Employee.objects.all()

    receipt_expense = None
    receipt_id = request.GET.get('receipt')
    show_all = request.GET.get('show') == 'all'

    if receipt_id:
        try:
            receipt_expense = Expense.objects.get(id=receipt_id)
        except Expense.DoesNotExist:
            receipt_expense = None

    if show_all:
        expenses = all_expenses
    else:
        expenses = all_expenses[:5]

    return render(request, 'expenses/list.html', {
        'expenses': expenses,
        'employees': employees,
        'receipt_expense': receipt_expense,
        'show_all': show_all,
    })

def add_expense(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee')
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        receipt = request.FILES.get('receipt')

        employee = Employee.objects.get(id=employee_id)

        Expense.objects.create(
            employee=employee,
            title=title,
            amount=amount,
            description=description,
            receipt=receipt
        )

        return redirect('expense_list')