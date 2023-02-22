from rest_framework.permissions import BasePermission


class OwnerOrStuff(BasePermission):

    def has_permission(self, request, view):
        if request.user == view.get_object().owner:
            return True
        if request.user.is_staff:
            return True
        return False


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        if request.user == view.get_object().owner:
            return True
        return False


class IsStaff(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class PermsForViewSetCourse(BasePermission):

    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list']:
            return request.user.is_authenticated or request.user.is_staff
        elif view.action == 'create':
            return request.user.is_authenticated and not request.user.is_staff
        elif view.action in ['update', 'partial_update', 'destroy']:
            if request.user == view.get_object().owner:
                return True
        else:
            return False


