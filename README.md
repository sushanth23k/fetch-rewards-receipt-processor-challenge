# Fetch Rewards Receipt Processor Challenge

## Overview
This web service is an assessment on Backend Engineering, where the goal was to create a web service that fulfills the provided API requirements. The service is designed to process receipts and manage user authentication and authorization.

## Project Components
- **Programming Language**: Python was chosen as the primary programming language due to familiarity and ease of use compared to Go.
- **Framework**: Django Framework was utilized to build a larger, more complex microservice that meets the requirements, rather than opting for a lightweight framework with fewer features.
- **Authentication**: Django Allauth Rest Framework was implemented for robust authentication, including optional social media integration.
- **Application Processing**: Gunicorn was used for application processing, managing worker nodes, timeout settings, and port binding.
- **Containerization**: A Docker container was built to install Python, MySQL, and the necessary packages from `requirements.txt`, and to run the Django server through WSGI, simulating a production environment.
- **Database**: MySQL was selected as the database for this project, hosted on a free service called "dash.filess.io". The database schema is documented in `DataBaseTables.sql`. 
  - **Note**: There are limitations with this service, such as the inability to handle multiple simultaneous database calls. This can be mitigated by using more robust database services like Cloud SQL (GCP) or Aurora DB (AWS).

## Code Base Architecture
- The main files, including `requirements.txt`, `Dockerfile`, and `gunicorn_config.py`, are located in the root folder.
- The entire Django codebase is organized within the `src` folder, along with environment variables.
- The Django application is segregated into three parts:

### Part 1: fetch_rewards
- This is the main Django folder containing essential files like `settings.py` and `wsgi.py`.
- A `router.py` file was created to route the admin page to the MySQL database instead of using SQLite.
- Allauth configuration, MySQL database connection, and admin page routing are set up in `settings.py`.

### Part 2: fetch_rewards_user
- This app was created to separate authentication and admin functionalities from the main use case of the project.
- Admin page URLs were established, and two users were created: one admin and one test user.
- Two permissions were created and attached to a new group, which was then assigned to the test user.
- Two wrapper functions were implemented: one for authentication using session ID and another for authorization based on permission ID.

### Part 3: fetch_rewards_receipt_processor
- A set of APIs was developed to meet the project requirements, with two sets of APIs designed for use with authentication and authorization.
- A wrapper function was created to validate input for both APIs.

## How to Use
1. **Set Up Environment**: Create a Python virtual environment and activate it.
2. **Install Requirements**: Run `pip install -r requirements.txt` to install necessary packages.
3. **Run Migrations**: Execute `python manage.py migrate --database Mysql` to set up the database.
4. **Start the Server**: Use `python manage.py runserver` to start the Django development server.
5. **Access APIs**: Use the provided APIs with the necessary authentication and authorization headers.

## Conclusion
This web service effectively addresses the provided API requirements while ensuring robust authentication and authorization mechanisms. The architecture is designed for scalability and maintainability, making it suitable for future enhancements and integrations.
