from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import datetime

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
def about (request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
     if request.method == "GET":
        return render(request, 'djangoapp/contact.html')
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            # If not, return to login page again
            context["message"] = "Bad inputs :\ "
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return render(request, 'djangoapp/index.html')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            context["message"] = f"Signed in sucessfully {username} !"
            return render(request, 'djangoapp/login.html', context)
        else:
            context["message"] = "You are already signed up !"
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    with open ("../functions/.creds-sample.json", 'r') as creds:
        data = json.load(creds)
    
    username = data["COUCH_USERNAME"]
    apikey = data ["IAM_API_KEY"]
    if request.method == "GET":
        url = f"https://9ad6410f.eu-gb.apigw.appdomain.cloud/api/dealership?COUCH_USERNAME={username}&IAM_API_KEY={apikey}"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    with open ("../functions/.creds-sample.json", 'r') as creds:
        data = json.load(creds)
    
    username = data["COUCH_USERNAME"]
    apikey = data ["IAM_API_KEY"]

    if request.method == "GET":
        url = f"https://9ad6410f.eu-gb.apigw.appdomain.cloud/api/review?COUCH_USERNAME={username}&IAM_API_KEY={apikey}&dealerId={dealer_id}"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url)
        # Concat all dealer's short name
        list_reviews = ' '.join([info_review.review for info_review in reviews])
        sentiment_reviews = ' '.join([info_review.sentiment for info_review in reviews])
        # Return a list of dealer short name
        return HttpResponse(f"{list_reviews} + {sentiment_reviews}")

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    with open ("../functions/.creds-sample.json", 'r') as creds:
        data = json.load(creds)
    
    username = data["COUCH_USERNAME"]
    apikey = data ["IAM_API_KEY"]
    if request.method == "GET":
        dealersid = dealer_id
        url = f"https://9ad6410f.eu-gb.apigw.appdomain.cloud/api/review?COUCH_USERNAME={username}&IAM_API_KEY={apikey}&dealerId={dealer_id}"
        # Get dealers from the URL
        context = {
            "cars": models.CarModel.objects.all(),
            "dealers": restapis.get_dealers_from_cf(url),
        }
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        if request.user.is_authenticated:
            form = request.POST
            review = {
                "name": "{request.user.first_name} {request.user.last_name}",
                "dealership": dealer_id,
                "review": form["content"],
                "purchase": form.get("purchasecheck"),
                }
            if form.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
                car = models.CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.carmake.name
                review["car_model"] = car.name
                review["car_year"]= car.year.strftime("%Y")
            json_payload = {"review": review}
            print (json_payload)
            url = f"https://9ad6410f.eu-gb.apigw.appdomain.cloud/api/review?COUCH_USERNAME={username}&IAM_API_KEY={apikey}&dealerId={dealer_id}"
            restapis.post_request(url, json_payload)
            return HttpResponse(f'review submitted : {json_payload}')
        else:
            return render(request, 'djangoapp/index.html', context)

