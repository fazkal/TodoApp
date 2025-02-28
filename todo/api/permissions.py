from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        '''Read permissions are allowed to any request
         if Todo Tasks Api List, display the tasks of all users'''
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user.user == request.user
        #return obj.user == request.user.profile 