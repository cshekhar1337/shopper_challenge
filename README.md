# shopper_challenge
## About the challenge
Instacart Shoppers are the face of the company - literally - and as such, we require them to go through a rigorous process before they can deliver your groceries. This includes a comprehensive application as well as a training process.
This challenge is broken into two parts. The first part is implementing the public-facing site that a prospective Instacart Shopper would see when hearing about the opportunities that Instacart offers. The second is writing analytics to monitor the progress of shoppers through the hiring funnel.

## Dependency
1. Python
2. django
3. sqlite3
Created using python version 3.6.0, django version 1.11 and sqlite3 version 3.13.0

## Steps for installation
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

** random data is generated by using date between   start_date = datetime.datetime(2014, 2, 1) and end_date = datetime.datetime(2017, 3, 1) which is end date for date generator. If you want change this go to instacart/shopper_challenge/views.py and then to function "def generate_random_date()" and change value of start_date and end_date manually
  **
## URL for the application
1. "http://127.0.0.1:8000/shopper_challenge/" -> Home page for shopper challenge app. This page has new shopper registeration interface and check status interface

2. "http://127.0.0.1:8000/shopper_challenge/bulk_upload/100" -> loads 100 random generated application

3."http://127.0.0.1:8000/shopper_challenge/funnel.json/?start_date=2013-7-5&end_date=2016-7-7" -> get analytics of the applicant within a time frame(start date to end date)

4. "http://127.0.0.1:8000/admin/" -> django admin view

## Design and tradeoffs
1. For fast analytics i have used django Local-memory caching. It stores key value pair of week and list of work_statuses count. This improves perfomance when same key is fetched again from system then we don't have to look into the database. This saves time.  Timeout for this cache is 300 seconds (5 minutes) and max_entries count is 300. 

2. Right now i have used ** sqlite3 ** as the question stated to use it. **It would be a good idea if we separate the database to another computing instance. I would prefer to use mysql instead. This will make our code truly scalable. We can run django application to serve request on many instances and contacting a database service like cloudsql(google app engine) which offers replication and backup on its own. **

3. We can increase the performance of analytics by indexing the database based on application_date as our queries are getting data between two dates. This will further improve the performance of the query

## Future work
1. write unit test
2. port the application to cloud
3. check for security related issues
4. add more functionality


