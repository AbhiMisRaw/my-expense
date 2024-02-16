import datetime


from django.shortcuts import render, redirect
from django.db.models import Sum

# for authenticaltion nd login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .forms import ExpenseForm
from .models import Expense


# Create your views here.


# @login_required(login_url="/accounts/login/")
# def index(request):
#     print(request.user.is_authenticated)
#     return render(request, "expense_app/index.html")


@login_required(redirect_field_name="")
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


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        print(f"Username : {username}, Password : {password}")

    return render(request, "expense_app/login.html")


def registeration_view(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect(
                "register"
            )  # Redirect back to the registration page with an error message
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            messages.success(request, "User created successfully. Please log in.")
            return redirect(
                "login"
            )  # Redirect to the login page with a success message

    return render(request, "expense_app/register.html")


def logout_view(request):
    logout(request)
    return redirect("login")
