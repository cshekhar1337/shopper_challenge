# shopper_challenge
## About the challenge
Instacart Shoppers are the face of the company - literally - and as such, we require them to go through a rigorous process before they can deliver your groceries. This includes a comprehensive application as well as a training process.
This challenge is broken into two parts. The first part is implementing the public-facing site that a prospective Instacart Shopper would see when hearing about the opportunities that Instacart offers. The second is writing analytics to monitor the progress of shoppers through the hiring funnel.

## Dependency
1. Python
2. django
3. sqlite3
Created using python version 3.6.0, django version 1.11 and sqlite3 version 3.13.0

##Steps for installation
1. "git clone https://github.com/cshekhar1337/shopper_challenge.git"
2. go to the folder and "cd shopper_challenge/instacart"
**Make migrations**
3. make migrations for the db by executing "python manage.py makemigrations"
4. execute "python manage.py makemigrations --name newmodel shopper_challenge"
5. execute "python manage.py migrate"
6. execute "python manage.py migrate --run-syncdb" this will create the tables
7. execute "python manage.py runserver" -- to run the app
8. On the browser and go to "http://127.0.0.1:8000/shopper_challenge/" to visit the landing page
9. To insert random entries to database. Go to "127.0.0.1:8000/shopper_challenge/bulk_upload/100" this will insert 100 enteries
10. To get analytics of the applicant within a time frame(All funnel buckets). Go to "http://127.0.0.1:8000/shopper_challenge/funnel.json/?start_date=2013-7-5&end_date=2016-7-7"


