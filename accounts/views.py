from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
import re
from django.contrib.auth import get_user_model
# Create your views here.


def index(request):
    return render(request, 'index.html')


def shop(request):
    return render(request, 'shop.html')


User = get_user_model()


def register_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        account_type = request.POST.get('account_type')

        # Validate inputs
        if not email or not first_name or not last_name or not password or not confirm_password or not account_type:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return redirect('register')

        user = User.objects.create_user(
            email=email, password=password, first_name=first_name, last_name=last_name)

        # Set account type
        if account_type == "buyer":
            user.is_buyer = True
        elif account_type == "seller":
            user.is_client = True

        user.save()

        messages.success(
            request, "Your account has been created successfully.")
        return redirect('login')

    return render(request, 'register.html')


def is_valid_email(email):
    """
    Validate an email address using regular expressions.

    :param email: Email address to validate
    :return: True if the email is valid, False otherwise
    """
    # Define the regex pattern for a valid email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Match the email against the regex pattern
    if re.match(email_regex, email):
        return True
    else:
        return False


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('index')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request, User)
