import datetime


from django.shortcuts import render, redirect
from django.db.models import Sum

from .forms import ExpenseForm
from .models import Expense


# Create your views here.


def index(request):
    return render(request, "expense_app/index.html")


def create_expense(requset):
    expense_form = ExpenseForm()
    if requset.method == "POST":
        expense = ExpenseForm(requset.POST)
        if expense.is_valid():
            expense.save()

    expenses = Expense.objects.all()
    total_expense = expenses.aggregate(Sum("amount"))

    # Calculating last year expenses

    last_year = datetime.date.today() - datetime.timedelta(days=365)
    last_year_expense = Expense.objects.filter(date__gt=last_year)
    yearly_expense = last_year_expense.aggregate(Sum("amount"))

    # for last month

    last_month = datetime.date.today() - datetime.timedelta(days=30)
    last_month_expense = Expense.objects.filter(date__gt=last_month)
    monthly_expense = last_month_expense.aggregate(Sum("amount"))

    # weekly expenses
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    last_week_expense = Expense.objects.filter(date__gt=last_week)
    weekly_expense = last_week_expense.aggregate(Sum("amount"))

    daily_sums = (
        Expense.objects.filter()
        .values("date")
        .order_by("date")
        .annotate(sum=Sum("amount"))
    )

    categorical_sums = (
        Expense.objects.filter()
        .values("category")
        .order_by("category")
        .annotate(sum=Sum("amount"))
    )
    print(categorical_sums)

    return render(
        requset,
        "expense_app/index.html",
        {
            "expense_form": expense_form,
            "expenses": expenses,
            "total_expense": total_expense,
            "yearly_expense": yearly_expense,
            "weekly_expense": weekly_expense,
            "monthly_expense": monthly_expense,
            "daily_sums": daily_sums,
            "categorical_sums": categorical_sums,
        },
    )


def edit(request, id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)

    if request.method == "POST":
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "expense_app/edit.html", {"expense_form": expense_form})


def delete(request, id):
    if request.method == "POST" and "delete" in request.POST:
        print("request recieved")
        expense = Expense.objects.get(id=id)
        expense.delete()

    return redirect("home")
