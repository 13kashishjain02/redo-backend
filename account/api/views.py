from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from account.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token

# Register

# Url: https://<your-domain>/api/register
@api_view(['POST', ])
def userregister(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
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

