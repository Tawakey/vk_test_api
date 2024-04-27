from rest_framework.permissions import BasePermission, SAFE_METHODS




class AuthenticatedPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action in ["create", 'update']:
            return request.user.is_authenticated
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user 