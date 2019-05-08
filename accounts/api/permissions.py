from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCurrentUserProfileOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.profile.id == request.resolver_match.kwargs.get('pk')


class IsCurrentUserProfile(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.id == request.resolver_match.kwargs.get('pk')