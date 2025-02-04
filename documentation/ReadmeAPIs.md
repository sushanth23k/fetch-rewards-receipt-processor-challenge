
API Documentation:

# Login:

POST Request:
URL: http://127.0.0.1:8000/user/_allauth/app/v1/auth/login
Request Body:
```json
{
"username": "test",
"password": "sushanth1234"
}
```
Response:
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

# Logout:

POST Request:
URL: http://127.0.0.1:8000/user/_allauth/app/v1/auth/session
Request Header:
```
X-Session-Token: edln59ucnyi2rx5p7ap42ih8s7wa0suf
```
Response:
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

# Process Receipt (Authenticated, Authorized):

POST Request:
URL: http://127.0.0.1:8000/process_receipt_auth/
Request Header:
```
X-Session-Token: edln59ucnyi2rx5p7ap42ih8s7wa0suf
```
Request Body:
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
Response:
```json
{
    "id": "50f60e79-2901-4114-87ae-0e8e3b859d24"
}
```


# Get Receipt Points (Authenticated, Authorized):

GET Request:
URL: http://127.0.0.1:8000/fetch_rewards_receipt_processor/get_receipt_points/{id}/
Request Header:
```
X-Session-Token: edln59ucnyi2rx5p7ap42ih8s7wa0suf
```
Response:
```json
{
    "points": 109
}
```

# Process Receipt (Unauthenticated, Unauthorized):

POST Request:
URL: http://127.0.0.1:8000/fetch_rewards_receipt_processor/process_receipt/
Request Body:
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
Response:
```json
{
    "id": "50f60e79-2901-4114-87ae-0e8e3b859d24"
}
```


# Get Receipt Points (Unauthenticated, Unauthorized):

GET Request:
URL: http://127.0.0.1:8000/fetch_rewards_receipt_processor/get_receipt_points/{id}/
Response:
```json
{
    "points": 109
}
```

