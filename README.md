# Vista_SLA_Dashboard
It is an SLA Monitoring Tool, which provide you the details of all SLA and It has several features like User Management, SLA Management and Account Management &amp; SLA Analysis

Please use below steps to run this project

Step 1: Create Virtual Enviroment (Optional)
    ==> pip install virtualenv
    ==> virtualenv vista
    ==> source vista/bin/activate

Step 2: Install Dependencies
    ==> pip install -r requirementx.txt

Step 3: Edit dev.env 
    ==> Please fill required details

Step 4: Create tables
    ==> python manage.py db init
    ==> python manage.py db migrate
    ==> python manage.py db upgrade
    
    ** I you get any error then check db connection details or analyze the error & debug

Step 5: Seeding Dummy data
    ==> python seed.py

Step 6: python run.py 

website: localhost:5000/login

Step 7: Register yourself
    ==> you might not receive message as sucess or reject
    ==>check terminal for confirmation mail

Step 8: Use admin account to approve request
    ==> username: admin
    ==> password: admin
    ==> Service Console request ==> pending ==> approve
    ==> See terminal for login password

Step 9: Login with your credentials
    ==> Password required change on first login

Step 10: You are done.

#Known issue
1. Message is not getting displayed when signup and password reset
2. Sla Dashboard is not functional
3. approval for add & update sla is not working
4. Mail is not working (getting connection error) , No code issue

# Let me Know
1. if you notice any bug apart from mentioned above, feel free to post comments.

