from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import numpy as np
import joblib

# Create your views here.

model = joblib.load("vehicle_price_predictor.pkl")

@login_required
def home(request):
    predicted_price = None
    error_message = None

    if request.method == 'POST':
        try:
            features = [
                float(request.POST["present_price"]),
                float(request.POST["kms_driven"]),
                int(request.POST["fuel_type"]),
                int(request.POST["seller_type"]),
                int(request.POST["transmission"]),
                int(request.POST["owner"]),
                int(request.POST["age"]),
            ]

            input_data = np.array(features, dtype=float).reshape(1, -1)
            predicted_price = model.predict(input_data)[0]
            predicted_price = round(predicted_price, 1)


        except Exception as e:
            error_message = f"Error: {str(e)}"

    return render(request, "home.html", {"predicted_price": predicted_price, "error_message": error_message})


def user_login(request):
    """Handle user login."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect to the home page
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")


def user_logout(request):
    """Handle user logout."""
    logout(request)
    return redirect("login")
