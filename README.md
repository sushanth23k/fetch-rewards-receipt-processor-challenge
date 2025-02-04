# Fetch Rewards Receipt Processor Challenge

## Overview
This web service is an assessment on Backend Engineering, where the goal was to create a web service that fulfills the provided API requirements. The service is designed to process receipts and manage user authentication and authorization.

## Project Components
- **Programming Language**: Python was chosen as the primary programming language due to familiarity and ease of use compared to Go.
- **Framework**: Django Framework was utilized to build a larger, more complex microservice that meets the requirements, rather than opting for a lightweight framework with fewer features.
- **Containerization**: A Docker container was built to install Python, MySQL, and the necessary packages from `requirements.txt`, and to run the Django server through WSGI, simulating a production environment.
- **Database**: MySQL was selected as the database for this project, hosted on a free service called "dash.filess.io". The database schema is documented in `DataBaseTables.sql`. 
- **Authentication**: Django Allauth Rest Framework was implemented for robust authentication, including optional social media integration.
- **Application Processing**: Gunicorn was used for application processing, managing worker nodes, timeout settings, and port binding.

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
1. **Run Docker**: Build and run the Docker container on your local machine or push it to a cloud Docker registry and run it on a cloud service like EC2(AWS) or Cloud run(GCP). For scalling we can use AWS ECS.
2. **Access APIs**: Once the Docker container is running, you will have access to the provided APIs with the necessary authentication and authorization headers.

## API Documentation

### Login:

#### POST Request:
##### URL: /user/_allauth/app/v1/auth/login
##### Request Body:
```json
{
"username": "test",
"password": "sushanth1234"
}
```
##### Response:
```json
{
    "status": 200,
    "data": {
        "user": {
            "id": 2,
            "display": "test",
            "has_usable_password": true,
            "email": "testuser@example.com",
            "username": "test"
        },
        "methods": [
            {
                "method": "password",
                "at": 1738636764.7377899,
                "username": "test"
            }
        ]
    },
    "meta": {
        "is_authenticated": true,
        "session_token": "edln59ucnyi2rx5p7ap42ih8s7wa0suf"
    }
}
```

### Logout:

#### POST Request:
##### URL: /user/_allauth/app/v1/auth/session
##### Request Header:
```
X-Session-Token: edln59ucnyi2rx5p7ap42ih8s7wa0suf
```
##### Response:
```json
{
    "status": 401,
    "data": {
        "flows": [
            {
                "id": "login"
            },
            {
                "id": "signup"
            }
        ]
    },
    "meta": {
        "is_authenticated": false
    }
}
```

### Process Receipt (Authenticated, Authorized):

#### POST Request:
##### URL: /process_receipt_auth/
##### Request Header:
```
X-Session-Token: edln59ucnyi2rx5p7ap42ih8s7wa0suf
```
##### Request Body:
```json
{
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}
```
##### Response:
```json
{
    "id": "50f60e79-2901-4114-87ae-0e8e3b859d24"
}
```


### Get Receipt Points (Authenticated, Authorized):

#### GET Request:
##### URL: /get_receipt_points/{id}/
##### Request Header:
```
X-Session-Token: edln59ucnyi2rx5p7ap42ih8s7wa0suf
```
##### Response:
```json
{
    "points": 109
}
```

### Process Receipt (Unauthenticated, Unauthorized):

#### POST Request:
##### URL: /process_receipt/
##### Request Body:
```json
{
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}
```
##### Response:
```json
{
    "id": "50f60e79-2901-4114-87ae-0e8e3b859d24"
}
```


### Get Receipt Points (Unauthenticated, Unauthorized):

#### GET Request:
##### URL: /get_receipt_points/{id}/
##### Response:
```json
{
    "points": 109
}
```


## Conclusion
This web service effectively addresses the provided API requirements of receiving a receipt, processing it, and getting the points while ensuring robust authentication and authorization mechanisms. The architecture is designed for scalability and maintainability, making it suitable for future enhancements and integrations.
