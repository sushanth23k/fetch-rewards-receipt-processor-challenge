from django.shortcuts import render
from django.db import connections
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from fetch_rewards_user.views import authenticate_session_token, permission_required
import json
import re
from datetime import datetime
import uuid
import math


# Validate the receipt data
def validate_receipt(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['retailer', 'purchaseDate', 'purchaseTime', 'items', 'total']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({'error': 'The receipt is invalid. Please verify input.'}, status=400)
            
            # Validate retailer format
            if not re.match(r'^[\w\s\-&]+$', data['retailer'].strip()):
                return JsonResponse({'error': 'The receipt is invalid. Please verify input.'}, status=400)
                
            # Validate purchase date format
            try:
                datetime.strptime(data['purchaseDate'], '%Y-%m-%d')
            except ValueError:
                return JsonResponse({'error': 'The receipt is invalid. Please verify input.'}, status=400)
                
            # Validate purchase time format (24-hour)
            try:
                datetime.strptime(data['purchaseTime'], '%H:%M')
            except ValueError:
                return JsonResponse({'error': 'The receipt is invalid. Please verify input.'}, status=400)
                
            # Validate items array
            if not isinstance(data['items'], list) or len(data['items']) < 1:
                return JsonResponse({'error': 'The receipt is invalid. Please verify input.'}, status=400)
                
            # Validate each item
            for item in data['items']:
                if not isinstance(item, dict):
                    return JsonResponse({'error': 'The receipt is invalid. Please verify input.'}, status=400)
                if 'shortDescription' not in item or 'price' not in item:
                    return JsonResponse({'error': 'The receipt is invalid. Please verify input.'}, status=400)
                if not re.match(r'^[\w\s\-]+$', item['shortDescription'].strip()):
                    return JsonResponse({'error': 'The receipt is invalid. Please verify input.'}, status=400)
                if not re.match(r'^\d+\.\d{2}$', str(item['price'])):
                    return JsonResponse({'error': 'The receipt is invalid. Please verify input.'}, status=400)
                    
            # Validate total format
            if not re.match(r'^\d+\.\d{2}$', str(data['total'])):
                return JsonResponse({'error': 'The receipt is invalid. Please verify input.'}, status=400)
                
            # Validate total matches sum of items
            items_total = sum(float(item['price']) for item in data['items'])
            if abs(float(data['total']) - items_total) > 0.01:  # Using small epsilon for float comparison
                return JsonResponse({'error': 'The receipt is invalid. Please verify input.'}, status=400)
                
            return view_func(request, *args, **kwargs)
            
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'error': 'The receipt is invalid. Please verify input.'}, status=400)
            
    return wrapper

# Validate the id
def validate_id(view_func):
    def wrapper(request, id, *args, **kwargs):
        """Validate if the id is a non-empty string."""
        if not re.match(r'^\S+$', id):
            return JsonResponse({"error": "Invalid ID format"}, status=400)
        return view_func(request, id, *args, **kwargs)
    return wrapper


# Authenticated and Authorized Receipts
# Process the receipt with authentication and authorization
@api_view(['POST'])
@validate_receipt
@authenticate_session_token
@permission_required('receipts_process')
def process_receipt_authentication_authorization(request):
    receipt_id = str(uuid.uuid4())
    data = json.loads(request.body)
    
    points = 0
    points_breakdown = []
    
    # One point for every alphanumeric character in the retailer name
    retailer_points = sum(c.isalnum() for c in data['retailer'])
    if retailer_points > 0:
        points += retailer_points
        points_breakdown.append(f"{retailer_points} points - retailer name has {retailer_points} characters")
    
    # 5 points for every two items on the receipt
    items_points = (len(data['items']) // 2) * 5
    if items_points > 0:
        points += items_points
        pairs = len(data['items']) // 2
        points_breakdown.append(f"{items_points} points - {len(data['items'])} items ({pairs} pairs @ 5 points each)")
    
    # Points for item descriptions divisible by 3
    for item in data['items']:
        desc_length = len(item['shortDescription'].strip())
        if desc_length % 3 == 0:
            item_points = math.ceil(float(item['price']) * 0.2)
            points += item_points
            points_breakdown.append(f"{item_points} Points - \"{item['shortDescription'].strip()}\" is {desc_length} characters (a multiple of 3)")
            points_breakdown.append(f"            item price of {item['price']} * 0.2 = {float(item['price']) * 0.2}, rounded up is {item_points} points")
    
    total = float(data['total'])
    
    # 50 points if the total is a round dollar amount with no cents
    if total.is_integer():
        points += 50
        points_breakdown.append("50 points - total is a round dollar amount")
        
    # 25 points if the total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25
        points_breakdown.append("25 points - total is a multiple of 0.25")
    
    # 5 points if the total is greater than 10.00
    if total > 10.00:
        points += 5
        points_breakdown.append("5 points - total is greater than $10.00")
        
    # 6 points if the day in the purchase date is odd
    purchase_date = datetime.strptime(data['purchaseDate'], '%Y-%m-%d')
    if purchase_date.day % 2 == 1:
        points += 6
        points_breakdown.append("6 points - purchase day is odd")
        
    # 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = datetime.strptime(data['purchaseTime'], '%H:%M').time()
    if datetime.strptime('14:00', '%H:%M').time() < purchase_time < datetime.strptime('16:00', '%H:%M').time():
        points += 10
        points_breakdown.append("10 points - purchase made between 2:00 PM and 4:00 PM")

    # Insert the receipt data into the database
    with connections['Mysql'].cursor() as cursor:
        cursor.execute("""
            INSERT INTO fetch_buffalodug.receipts (id, retailer, purchaseDate, purchaseTime, total, points)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (receipt_id, data['retailer'], data['purchaseDate'], data['purchaseTime'], data['total'], points))

    # Commit the transaction
    connections['Mysql'].commit()

    return JsonResponse({
        'id': receipt_id
    })


# Unauthenticated and Unauthorized Receipts
# Get the receipt points with authentication and authorization
@api_view(['GET'])  
@validate_id
@authenticate_session_token
@permission_required('receipts_points')
def get_receipt_points_authentication_authorization(request, id):
    try:
        with connections['Mysql'].cursor() as cursor:
            cursor.execute("SELECT points FROM fetch_buffalodug.receipts WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                points = result[0]
                return JsonResponse({"points": points}, status=200)
            else:
                return JsonResponse({"error": "No receipt found for that ID."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Process the receipt without authentication and authorization
@api_view(['POST'])
@validate_receipt
def process_receipt_unauthentication_unauthorization(request):
    receipt_id = str(uuid.uuid4())
    data = json.loads(request.body)
    
    points = 0
    points_breakdown = []
    
    # One point for every alphanumeric character in the retailer name
    retailer_points = sum(c.isalnum() for c in data['retailer'])
    if retailer_points > 0:
        points += retailer_points
        points_breakdown.append(f"{retailer_points} points - retailer name has {retailer_points} characters")
    
    # 5 points for every two items on the receipt
    items_points = (len(data['items']) // 2) * 5
    if items_points > 0:
        points += items_points
        pairs = len(data['items']) // 2
        points_breakdown.append(f"{items_points} points - {len(data['items'])} items ({pairs} pairs @ 5 points each)")
    
    # Points for item descriptions divisible by 3
    for item in data['items']:
        desc_length = len(item['shortDescription'].strip())
        if desc_length % 3 == 0:
            item_points = math.ceil(float(item['price']) * 0.2)
            points += item_points
            points_breakdown.append(f"{item_points} Points - \"{item['shortDescription'].strip()}\" is {desc_length} characters (a multiple of 3)")
            points_breakdown.append(f"            item price of {item['price']} * 0.2 = {float(item['price']) * 0.2}, rounded up is {item_points} points")
    
    total = float(data['total'])
    
    # 50 points if the total is a round dollar amount with no cents
    if total.is_integer():
        points += 50
        points_breakdown.append("50 points - total is a round dollar amount")
        
    # 25 points if the total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25
        points_breakdown.append("25 points - total is a multiple of 0.25")
    
    # 5 points if the total is greater than 10.00
    if total > 10.00:
        points += 5
        points_breakdown.append("5 points - total is greater than $10.00")
        
    # 6 points if the day in the purchase date is odd
    purchase_date = datetime.strptime(data['purchaseDate'], '%Y-%m-%d')
    if purchase_date.day % 2 == 1:
        points += 6
        points_breakdown.append("6 points - purchase day is odd")
        
    # 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = datetime.strptime(data['purchaseTime'], '%H:%M').time()
    if datetime.strptime('14:00', '%H:%M').time() < purchase_time < datetime.strptime('16:00', '%H:%M').time():
        points += 10
        points_breakdown.append("10 points - purchase made between 2:00 PM and 4:00 PM")

    # Insert the receipt data into the database
    with connections['Mysql'].cursor() as cursor:
        cursor.execute("""
            INSERT INTO fetch_buffalodug.receipts (id, retailer, purchaseDate, purchaseTime, total, points)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (receipt_id, data['retailer'], data['purchaseDate'], data['purchaseTime'], data['total'], points))

    # Commit the transaction
    connections['Mysql'].commit()

    return JsonResponse({
        'id': receipt_id
    })


# Get the receipt points without authentication and authorization
@api_view(['GET'])  
@validate_id
def get_receipt_points_unauthentication_unauthorization(request, id):
    try:
        with connections['Mysql'].cursor() as cursor:
            cursor.execute("SELECT points FROM fetch_buffalodug.receipts WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                points = result[0]
                return JsonResponse({"points": points}, status=200)
            else:
                return JsonResponse({"error": "No receipt found for that ID."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Create your views here.