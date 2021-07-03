from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from account.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes,authentication_classes

# Register

# Url: https://<your-domain>/api/register

@api_view(['POST',])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def userregister(request):
    print("hello")
    print("hello",request.method)
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        print("hiiii")
        print(request.data)
        print(serializer)
        if serializer.is_valid():
            print("valid")
            account = serializer.save()
            data['response'] = 'successfully registered new user.'
            data['email'] = account.email
            data['name'] = account.name
            data['contact_number'] = account.contact_number

            token = Token.objects.get(user=account).key

            data['token'] = token

        else:
            data = serializer.errors

        return Response(data)

