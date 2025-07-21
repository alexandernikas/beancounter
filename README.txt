## INSTRUCTIONS TO RUN LOCALLY

    ## RUN DJANGO BACKEND
    1. Download files from branch beancounter/localhost-bundle or main
    2. Run your selected database (i.e., brew services start postgresql@15)
    3. Create a .env file in /backend following the provided sample
    4. Navigate to the /backend folder
    5. Create a venv
        5.1. >>>python -m venv env
    6. Activate venv (source env/bin/activate on mac/linux or env\Scripts\activate on Windows)
    7. Install requirements.txt
        7.1. >>>python -m pip install -r requirements.txt
    8. Create BEAN_COUNTER schema or select a different schema in settings.py
        8.1. sql CREATE SCHEMA IF NOT EXISTS BEAN_COUNTER AUTHORIZATION <username>;
    9. Run migrations
        9.1. >>>python manage.py makemigrations
        9.2. >>>python manage.py migrate
    10. Run development server
        10.1. >>>python manage.py runserver
    
    ## RUN VUE FRONTEND
    11. Navigate to beancounter_frontend
    12. Create a .env file in /beancounter_frontend following the provided sample
    13. Run "npm install"
    14. Run "npm run serve"
    15. Check that the app is running; https://your-local-frontend-url/home is the route for the landing page

## USER INSTRUCTIONS
1. In the web client, navigate to the "Manage Coffee Menu" button on the sidebar
2. On the coffee menu page, hit "Update Prices". This will retrieve the coffee menu from a local Broomfield coffee shop (robots.txt was reviewed to ensure compliance with terms of services)
3. In the web client, navigate to the "Manage Team Members" button on the sidebar and add team members. Hit "Save Changes" to post additions/updates to database.
4. To submit a coffee run, select the purchaser in the top right dropdown and hit "Submit".
5. To account for absences, select the "Out of Office" checkbox on the left hand table. OOO members will be excluded from the transaction and suggested buyer.
6. To review a transaction, click the transaction on the "Recent Coffee Runs" table
8. To roll back a transaction, hit "Delete Transaction" on the transaction-detail page.

## ACCESSING THE CLOUD INSTANCE
The app is hosted on Azure here -> https://polite-sky-0deb0790f.2.azurestaticapps.net/home

## CORE ASSUMPTIONS
1. Team members' orders are predictable and consistent
2. The team always visits the same coffee shop
3. Team members will not settle balances individually,
   and instead rely solely on a round-robin style ordering system 
   to ensure an equitable purchasing cadence