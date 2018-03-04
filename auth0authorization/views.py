import os
import jwt
import json
from functools import wraps

from django.http import JsonResponse
from rest_framework.decorators import api_view
from six.moves.urllib import request as req
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .serializers import CountrySerializer
from .models import City, Country

# Create your views here.


def get_token_auth_header(request):
    """Obtains the access token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]
    print('Found authorization !!! Bearer {}'.format(token))

    return token


def requires_scope(required_scope):
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    def require_scope(f):
        print('in require_scope')
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
            print('AUTH0_DOMAIN : {}'.format(AUTH0_DOMAIN))

            API_IDENTIFIER = os.environ.get('API_IDENTIFIER')
            jsonurl = req.urlopen('https://' + AUTH0_DOMAIN + '/.well-known/jwks.json')
            jwks = json.loads(jsonurl.read())
            cert = '-----BEGIN CERTIFICATE-----\n' + jwks['keys'][0]['x5c'][0] + '\n-----END CERTIFICATE-----'
            certificate = load_pem_x509_certificate(cert.encode('utf-8'), default_backend())
            public_key = certificate.public_key()
            decoded = jwt.decode(token, public_key, audience=API_IDENTIFIER, algorithms=['RS256'])

            if certificate:
                print('Cert Serial : {}'.format(certificate.serial_number))

            if decoded:
                for k,v in decoded.items():
                    print('{} : {}'.format(k,v))

            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse({'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response
        return decorated
    return require_scope


class CountryListAPIView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = CountrySerializer(queryset, many=True)
        return Response(serializer.data)


def public(request):
    return JsonResponse({'message': 'Hello from a public endpoint! You don\'t need to be authenticated to see this.'})


@api_view(['GET'])
def private(request):
    return JsonResponse({'message': 'Hello from a private endpoint! You need to be authenticated to see this.'})


@api_view(['GET'])
@requires_scope('read:messages')
def private_scoped(request):
    return JsonResponse({'message': 'Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this.'})

@api_view(['GET'])
@requires_scope('write:messages')
def private_scoped_write(request):
    return JsonResponse({'message': 'Hello from a private endpoint! You need to be authenticated and have a scope of write:messages to see this.'})
