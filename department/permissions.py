from rest_framework.permissions import BasePermission


class OwnerOrStuff(BasePermission):

    def has_permission(self, request, view):
        if request.user == view.get_object().owner:
            return True
        if request.user.role == 'moderator':
            return True
        return False


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        if request.user == view.get_object().owner:
            return True
        return False


class IsStaff(BasePermission):

    def has_permission(self, request, view):
        if request.user.role == 'moderator':
            return True
        return False


class IsNotStaff(BasePermission):

    def has_permission(self, request, view):
        if request.user.role != 'moderator':
            return True
        return False


class PermsForViewSetCourse(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list']:
            return request.user.is_authenticated or request.user.role == 'moderator'
        elif view.action in ['create', 'destroy']:
            return request.user.is_authenticated and not request.user.role == 'moderator'
        elif view.action in ['update', 'partial_update']:
            if request.user == view.get_object().owner or request.user.role == 'moderator':
                return True
        else:
            return False
