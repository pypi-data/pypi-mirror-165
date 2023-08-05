from django.shortcuts import render

from django.http import HttpResponse,FileResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse


import jwt
from functools import wraps

from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

def get_token_auth_header(request):
    """Obtains the access token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    if auth:
        parts = auth.split()
        token = parts[1]

        return token
    return None


def requires_scope(required_scope):
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            if not token:
                # 没有认证
                response = JsonResponse({'message': 'You don\'t have access to this resource, need token'})
                response.status_code = 403
                return response
            
            # 检查权限scope
            decoded = jwt.decode(token, verify=False)
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

def index(request):
    return HttpResponse("demo home")

@requires_scope('read:messages')
def protected_page(request):
    token = get_token_auth_header(request)
    return HttpResponse(token)



