from rest_framework import permissions


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.staff


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.staff

class AdvancedUserManage(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.advanced_user
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.advanced_user
