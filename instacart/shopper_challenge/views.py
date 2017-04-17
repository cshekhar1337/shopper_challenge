from django.shortcuts import render, redirect
import random, string, time, datetime
import collections,json
from django.db.models import Count

from collections import OrderedDict


from django.http import HttpResponse, HttpResponseBadRequest
from .models import Applicant




# List of workflow_states to pick from for seed data
WORKFLOW_STATES = [ "quiz_started", "quiz_completed", "applied","onboarding_requested", "onboarding_completed", "hired", "rejected"]

# List of some locations to pick from for seed data
CITY_STATE_MAP = {'Los Angeles': 'California', 'Houston' : 'Texas', 'San Francisco': 'California', 'Miami': 'Florida', 'Cleveland': 'Ohio', 'San Jose': 'California', 'Austin' : 'Texas', 'Detroit': 'Michigan', 'Las Vegas': 'Nevada', 'Cincinnati' : 'Ohio', 'Madison': 'Wisconsin', 'Tempe': 'Arizona'}
####################################################################
# functions for creating random data
####################################################################
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
#########################################################################################################

####################################################################
# utility functions for creating funnel
####################################################################
def get_funnel_all_weeks(start_date, end_date):
    closest_prev_monday = get_closest_prev_monday(start_date)
    closest_next_sunday = get_closest_next_sunday(end_date)

    weekly_dict = OrderedDict()
    curr_date = closest_prev_monday
    while curr_date <= closest_next_sunday:
        #Dictionary here contains kv pairs of {Monday, next Sunday}
        weekly_dict[curr_date] = curr_date + datetime.timedelta(days=6)
        #Increment it to the next monday (+7 days)
        curr_date += datetime.timedelta(days=7)

    return weekly_dict

def get_week_key(week_start, week_end):
    return str(week_start) + "-" + str(week_end)



def get_closest_prev_monday(date):
    return (date - datetime.timedelta(days=int(date.weekday())))

def get_closest_next_sunday(date):
    return (date + datetime.timedelta(days=6-int(date.weekday())))

def generate_funnel_report(request_params):

    try:
        start_date_str = request_params['start_date']



        end_date_str = request_params['end_date']

        print("Start date---",  start_date_str )
        print("End date---",  end_date_str )
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
        print("----jflsj", start_date.year)
        end_date = datetime.datetime.strptime(end_date_str , '%Y-%m-%d')

    except Exception as e:
        errorprint("Input dates are invalid. Please check and try again. Input is start_date: " + start_date_str + ", end_date: " + end_date_str)

    # Check if start_date > end_date, then input is invalid. Start date should be less than or equal to end date
    if start_date > end_date:
        errorprint("Input dates are invalid. start_date cannot be after end_date")

    # OrderedDict to maintain the order of weeks
    funnel_metrics = collections.OrderedDict()
    all_weeks = get_funnel_all_weeks(start_date, end_date)



    for week_start, week_end in all_weeks.items():
        week_key = get_week_key(week_start, week_end)
        weekly_workflow_stats = {}


        if not weekly_workflow_stats:
            shoppers_states = Applicant.objects.filter(application_date__gte=week_start, application_date__lte=week_end).values('workflow_state').annotate(count=Count('workflow_state'))

            if shoppers_states:
                weekly_workflow_stats = {}
                for state in shoppers_states:
                    weekly_workflow_stats[state['workflow_state']] = state['count']



        if weekly_workflow_stats:
            funnel_metrics[week_key] = weekly_workflow_stats

    return funnel_metrics



#####################################################################

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
    try:
        request_params = request.GET
        if len(request_params) != 2:
            errorprint("Input params are invalid. API expects 2 params. Provided " + str(len(request_params)) + " params")

        funnel_report = generate_funnel_report(request_params)

        return HttpResponse(json.dumps(funnel_report, indent = 7), content_type="application/json")
    except Exception as e:
        return errorprint(str(e))




def errorpage(request):
    return HttpResponse("Sorry something went wrong.. Error " )

def errorprint(message):
    return HttpResponse("Sorry something went wrong.. Error " + message)






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







