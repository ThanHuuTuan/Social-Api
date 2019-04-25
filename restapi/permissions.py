from rest_framework import permissions

class IsGroupAdmin(permissions.BasePermission):
	def has_permission(self, request, view):
		pass
	#end
#end
