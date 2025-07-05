from django.shortcuts import render
from django.http import JsonResponse
from .models import FirebaseUser
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def save_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')

            if not name or not email:
                return JsonResponse({'error': "Name and email are required"}, status=400)

            user, created = FirebaseUser.objects.get_or_create(
                email=email, defaults={'name': name})

            return JsonResponse({'message': "User saved successfully", 'created': created})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': "Only POST method is allowed"}, status=405)
