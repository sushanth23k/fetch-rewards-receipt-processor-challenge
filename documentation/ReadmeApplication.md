# Fetch Rewards Receipt Processor Challenge

# Creating a python virtual ennvironment
python3 -m venv venv .

# Activate Virtual Ennvironment
source venv/bin/activate 

# Basic Requirements Install 
pip3 install -r requirements.txt

# Start Project
### Inside src folder run this command
django-admin startproject fetch_rewards .

# Command to start Djnago Server
python manage.py runserver

# Command to create a new app
python manage.py startapp fetch_rewards_receipt_processor

# Command to make create SQL using makemigrations
python manage.py makemigrations

# Command to execute the migrations
python manage.py migrate --database Mysql

# Rivertback Migrations 
python manage.py migrate your_app zero
python manage.py migrate your_app 0001

# Delete all Migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

# Migrate only certain app
python manage.py makemigrations fetch_rewards_receipt_processor

# Super User creation
python manage.py createsuperuser

# Git commit and push command
git add . && git commit -a -m "commit" && git push


# Mysql Hosting URL
[Database hosting](https://cp1.awardspace.net/database-manager/)
[DataBase Hosting](https://dash.filess.io/#/app/databases/v1/0d150f34-e44d-4a69-bc95-cc510f266e2d)

# Resolving Problems
[Docker Not working in MacOs](https://stackoverflow.com/questions/79340672)

# Allauth Documentation
[Allauth Documentation](https://allauth.org/docs/draft-api/#tag/Configuration)