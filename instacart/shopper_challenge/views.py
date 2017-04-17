from django.shortcuts import render, redirect
import random, string, time, datetime

from django.http import HttpResponse, HttpResponseBadRequest
from .models import Applicant



# List of workflow_states to pick from for seed data
WORKFLOW_STATES = [ "quiz_started", "quiz_completed", "applied","onboarding_requested", "onboarding_completed", "hired", "rejected"]

# List of some locations to pick from for seed data
CITY_STATE_MAP = {'Los Angeles': 'California', 'Houston' : 'Texas', 'San Francisco': 'California', 'Miami': 'Florida', 'Cleveland': 'Ohio', 'San Jose': 'California', 'Austin' : 'Texas', 'Detroit': 'Michigan', 'Las Vegas': 'Nevada', 'Cincinnati' : 'Ohio', 'Madison': 'Wisconsin', 'Tempe': 'Arizona'}
####################################################################
# functions for creating random data
####################################
def generate_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def generate_random_place():
    return random.choice(list(CITY_STATE_MAP.keys()))

def generate_random_number(length):
    lower = 10**(length-1)
    upper = 10**length - 1
    return random.randint(lower, upper)

def generate_random_date():
    start_date = datetime.datetime(2014,2,1)   # start date for date generator
    end_date = datetime.datetime(2017,3, 1)    # end date for date generator
    tot_days = (end_date -start_date).days
    rand_day = random.randint(1, tot_days)
    random_date = (start_date + datetime.timedelta(rand_day)).strftime("%Y-%m-%d")
    return random_date

def generate_random_status():
    return random.choice(WORKFLOW_STATES)


#########################################################################################################

def home(request):
    return HttpResponse("Hello, world!" )




def signup(request):
    return HttpResponse("Hello, world!")




def signup_success(request):
    return HttpResponse("Hello, world!")




def check_status(request):
    return HttpResponse("Hello, world!")




def edit(request):
    return HttpResponse("Hello, world!")




def update(request):
    return HttpResponse("Hello, world!")




def logout(request):
    return HttpResponse("Hello, world!")




def funnel(request):
    return HttpResponse("Hello, world!")




def errorpage(request):
    return HttpResponse("Hello, world!")




def bulk_upload(request, count):
    # count of users saved in db
    registeredCount = 0
    entries_required = int(count)

    # total no of tries it will make to enter the records
    max_tries = entries_required + 80

    for i in range(max_tries):
        # If we have generated given count of test shoppers, break
        if registeredCount > entries_required:
            break

        name = generate_random_string(10)
        email = generate_random_string(10) + '@gmail.com'
        phone = generate_random_number(10)
        city = generate_random_place()
        state = CITY_STATE_MAP[city]
        date_applied = generate_random_date()
        status = generate_random_status()
        shopper = Applicant(name=name, email=email, phone=phone, city=city, state=state, application_date=date_applied, workflow_state=status)

        # Verify that same email or phone numbers are not inserted again
        if not Applicant.objects.filter(email=email).exists() and not Applicant.objects.filter(phone=phone).exists():
            registeredCount += 1
            shopper.save()

    return HttpResponse('bulk upload done!!. No of registered applicant created = ' + str(registeredCount -1))







