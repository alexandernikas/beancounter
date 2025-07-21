## INSTRUCTIONS TO RUN LOCALLY
Download files from branch beancounter/localhost-bundle or main
run your selected database (app is currently configured for postgresql)
create a .env file in /backend following the provided sample
Cd backend
Create venv
Activate venv (source env/bin/activate on mac/linux or env\Scripts\activate on Windows)
Install requirements.txt
CREATE BEAN_COUNTER schema
CREATE SCHEMA IF NOT EXISTS BEAN_COUNTER
    AUTHORIZATION <username>;
Python manage.py make migrations
Python manage.py migrate
Python manage.py runserver // backend up and running

Navigate beancounter_frontend
create a .env file in /beancounter_frontend following the provided sample
NPM install
NPM run serve

In client
Load products
Add employees
Add transactions


## CORE ASSUMPTIONS