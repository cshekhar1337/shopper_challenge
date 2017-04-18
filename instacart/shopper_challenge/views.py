from django.shortcuts import render, redirect
import random, string, time, datetime
import collections, json
from django.contrib import messages
from django.db.models import Count
from django.core.cache import cache
from collections import OrderedDict
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Applicant

# List of workflow_states to needed to created random data
WORKFLOW_STATES = ["quiz_started", "quiz_completed", "applied", "onboarding_requested", "onboarding_completed", "hired",
                   "rejected"]

# List of city state mapping needed for data insertion purposes
CITY_STATE_MAP = {'Los Angeles': 'California', 'Houston': 'Texas', 'San Francisco': 'California', 'Miami': 'Florida',
                  'Cleveland': 'Ohio', 'San Jose': 'California', 'Austin': 'Texas', 'Detroit': 'Michigan',
                  'Las Vegas': 'Nevada', 'Cincinnati': 'Ohio', 'Madison': 'Wisconsin', 'Tempe': 'Arizona'}


def home(request):
    '''renders home page for the shopper_challenge app'''
    return render(request, 'shopper_challenge/login_signup.html')


def signup(request):
    ''' handler that check whether phone and email already exists or not. If not, direct to terms_agreement page'''

    if request.POST:
        # Obtain form data from the request and store in session variables so they can be accessed across functions
        user_info = request.POST
        is_valid_user = True

        if Applicant.objects.filter(email=user_info['email']).exists():
            is_valid_user = False
            error_message = "This email is already registered!"

            messages.add_message(request, messages.ERROR, error_message)

        if Applicant.objects.filter(phone=user_info['phone']).exists():
            is_valid_user = False
            error_message = "This phone number is already registered!"
            messages.add_message(request, messages.ERROR, error_message)

        if not is_valid_user:
            return render(request, 'shopper_challenge/login_signup.html')

        # If the user is valid, set the user session details
        request.session['name'] = user_info['name']
        request.session['email'] = user_info['email']
        request.session['phone'] = user_info['phone']
        request.session['city'] = user_info['city']
        request.session['state'] = user_info['state']

        # Redirect the user to background check consent form
        return render(request, 'shopper_challenge/terms_agreement.html')


def signup_success(request):
    ''' handler that saves applicant info to the database and renders success page'''
    if request.POST:
        # Check if the user is already registered
        shopper = Applicant.objects.filter(email=request.session['email'])
        if shopper:
            return render(request, 'shopper_challenge/application_success_page.html', shopper[0].__dict__)

        # Register the user and save user information in database
        name = request.session['name']
        email = request.session['email']
        phone = request.session['phone']
        city = request.session['city']
        state = request.session['state']

        shopper = Applicant(name=name, email=email, phone=phone, city=city, state=state)
        shopper.save()

        # Delete all user's session data except for 'email' which is used to maintain user-session
        del request.session['name']
        del request.session['phone']
        del request.session['city']
        del request.session['state']

        # Redirect user to the registration confirmation page
        return render(request, 'shopper_challenge/application_success_page.html', shopper.__dict__)


def check_status(request):
    ''' handler to check status of the applicant based on the email id '''
    if request.POST:
        email = request.POST['email']
        if not email:
            error_message = "Please enter a valid email."
            messages.add_message(request, messages.ERROR, error_message)
            return render(request, 'shopper_challenge/login_signup.html')
        else:
            if (Applicant.objects.filter(email=email).exists()):
                shopper = Applicant.objects.filter(email=email)[0]

                # Set the user's email in session
                request.session['email'] = shopper.email
                return render(request, 'shopper_challenge/applicant_view.html', shopper.__dict__)
            else:
                messages.add_message(request, messages.ERROR, "No application associated with this email")
                return render(request, 'shopper_challenge/login_signup.html')


def edit(request):
    ''' handler to edit applicant info by sending the info to update handler'''
    shopper = Applicant.objects.filter(email=request.session['email'])
    # print(shopper[0].__dict__)
    return render(request, 'shopper_challenge/update_application.html', shopper[0].__dict__)


def update(request):
    ''' handler to update the applicant info '''
    # Fetch the user details from db based on session.email key
    shopper = Applicant.objects.filter(email=request.session['email'])[0]

    if shopper.phone != request.POST['phone'] and Applicant.objects.filter(phone=int(request.POST['phone'])).exists():
        messages.add_message(request, messages.ERROR, "Phone number already registered with a different user")
        return render(request, 'shopper_challenge/update_application.html', shopper.__dict__)

    '''
    If user update is valid, update all fields except email.
    '''
    shopper.name = request.POST['name']
    shopper.phone = request.POST['phone']
    shopper.city = request.POST['city']
    shopper.state = request.POST['state']
    shopper.save()
    return render(request, 'shopper_challenge/applicant_view.html', shopper.__dict__)


def logout(request):
    ''' handler that deletes session and redirects to signup page'''

    del request.session['email']
    return render(request, 'shopper_challenge/login_signup.html')


def funnel(request):
    ''' handler function that generates the funnel buckets and sends the formatted json as response'''
    try:
        request_params = request.GET
        if len(request_params) != 2:
            errorprint(
                "Input params are invalid. API expects 2 params. Provided " + str(len(request_params)) + " params")

        funnel_report = generate_funnel_buckets(request_params)

        return HttpResponse(json.dumps(funnel_report, indent=7), content_type="application/json")
    except Exception as e:
        return errorprint(str(e))


def errorpage(request):
    ''' error page'''
    return HttpResponse("Sorry something went wrong.. Error ")


def errorprint(message):
    ''' general error page that prints the message passed to it'''
    return HttpResponse("Sorry something went wrong.. Error " + message)


def bulk_upload(request, count):
    ''' adds applicant to database using random values generated'''
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
        shopper = Applicant(name=name, email=email, phone=phone, city=city, state=state, application_date=date_applied,
                            workflow_state=status)

        # Verify that same email or phone numbers are not inserted again
        if not Applicant.objects.filter(email=email).exists() and not Applicant.objects.filter(phone=phone).exists():
            registeredCount += 1
            shopper.save()

    return HttpResponse('bulk upload done!!. No of registered applicant created = ' + str(registeredCount - 1))


def invalidate_cache(date):
    ''' remove a entry from cache corresponding to the date provided'''
    closest_prev_monday = get_closest_prev_monday(date)
    closest_next_sunday = get_closest_next_sunday(date)
    key = get_week_key(closest_prev_monday.strftime("%Y-%m-%d").date(), closest_next_sunday.strftime("%Y-%m-%d"))
    cache.delete(key)


####################################################################
# functions for creating random data
####################################################################
def generate_random_string(length):
    ''' returns string of specified length'''
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def generate_random_place():
    '''returns a random city'''
    return random.choice(list(CITY_STATE_MAP.keys()))


def generate_random_number(length):
    ''' generates a random of length passed to it'''
    lower = 10 ** (length - 1)
    upper = 10 ** length - 1
    return random.randint(lower, upper)


def generate_random_date():
    ''' generates a random date that  corresponds to application_date of the applicant'''
    start_date = datetime.datetime(2014, 2, 1)  # start date for date generator
    end_date = datetime.datetime(2017, 3, 1)  # end date for date generator
    tot_days = (end_date - start_date).days
    rand_day = random.randint(1, tot_days)
    random_date = (start_date + datetime.timedelta(rand_day)).strftime("%Y-%m-%d")
    return random_date


def generate_random_status():
    ''' generates a random workflow state'''
    return random.choice(WORKFLOW_STATES)


#########################################################################################################
#########################################################################################################

####################################################################
# utility functions for creating funnel
####################################################################
def get_funnel_all_weeks(start_date, end_date):
    ''' returns a ordered dictionary of all the weeks that lies between the start date and end date'''
    closest_prev_monday = get_closest_prev_monday(start_date)
    closest_next_sunday = get_closest_next_sunday(end_date)

    weekly_dict = OrderedDict()
    curr_date = closest_prev_monday
    while curr_date <= closest_next_sunday:
        weekly_dict[curr_date] = curr_date + datetime.timedelta(days=6)
        # Increment it to the next monday (+7 days)
        curr_date += datetime.timedelta(days=7)

    return weekly_dict


def get_week_key(week_start, week_end):
    ''' returns a string that is used for map. string is combination of week_start and week_end'''
    return str(week_start) + "-" + str(week_end)


def get_closest_prev_monday(date):
    ''' returns datetime object corresponding to  week start. assuming week start at monday and end at sunday'''
    return (date - datetime.timedelta(days=int(date.weekday())))


def get_closest_next_sunday(date):
    ''' returns datetime object corresponding to  week end. assuming week start at monday and end at sunday'''

    return (date + datetime.timedelta(days=6 - int(date.weekday())))


def generate_funnel_buckets(request_params):
    ''' generates a dictionary with key(closestprevmonday-closestnextsunday) and value= list of workflow states in that period '''

    try:
        start_date_str = request_params['start_date']

        end_date_str = request_params['end_date']

        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()

        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except Exception as e:
        errorprint(
            "Input dates are invalid. Please check and try again. Input is start_date: " + start_date_str + ", end_date: " + end_date_str)
    # Check if start_date > end_date, then input is invalid. Start date should be less than or equal to end date
    if start_date > end_date:
        errorprint("Input dates are invalid. start_date cannot be after end_date")

    # OrderedDict to maintain the order of weeks
    funnel_buckets = collections.OrderedDict()

    all_weeks = get_funnel_all_weeks(start_date, end_date)

    for week_start, week_end in all_weeks.items():
        week_key = get_week_key(week_start, week_end)

        weekly_workflow_stats = cache.get(week_key)
        if not weekly_workflow_stats:
            shoppers_states = Applicant.objects.filter(application_date__gte=week_start,
                                                       application_date__lte=week_end).values(
                'workflow_state').annotate(count=Count('workflow_state'))

            if shoppers_states:
                weekly_workflow_stats = { "applied": 0, "quiz_started": 0, "quiz_completed": 0,
                                         "onboarding_requested": 0, "onboarding_completed": 0, "hired": 0,
                                         "rejected": 0}
                for state in shoppers_states:
                    weekly_workflow_stats[state['workflow_state']] = state['count']

                cache.set(week_key, weekly_workflow_stats)

        if weekly_workflow_stats:
            funnel_buckets[week_key] = weekly_workflow_stats

    return funnel_buckets

#####################################################################
#####################################################################
