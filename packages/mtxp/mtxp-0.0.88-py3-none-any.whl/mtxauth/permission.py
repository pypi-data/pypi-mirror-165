from rest_framework import permissions
from mtlibs.cognito_util import jwt_decode_token
import jwt
# 自定义访问权限

class MtxJwtPermission(permissions.BasePermission):
    """校验jwt"""
    def has_permission(self, request, view):
        try:
            token = request.headers.get("Authorization",None) or request.headers.get("mtxtoken",None)
            if not token:
                return False
            # decoded_token = jwt_decode_token(token)
            # print(f"decoded_token {decoded_token}")
            return True
        except jwt.exceptions.ExpiredSignatureError as e:
            print("jwt已经过期")
            return False
        except Exception as err:
            print("未知jwt 错误", err)
            raise err

# class MtxPermission(permissions.BasePermission):
#     """
#     Object-level permission to only allow owners of an object to edit it.
#     Assumes the model instance has an `owner` attribute.
#     """
#     def has_permission(self, request, view):
#         ip_addr = request.META['REMOTE_ADDR']
#         # blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()
#         return True
    
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         # Instance must have an attribute named `owner`.
#         return obj.owner == request.user

