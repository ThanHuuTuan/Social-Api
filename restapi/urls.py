"""restapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from rest_framework import routers
from . import views
from django.contrib import admin
from rest_framework.authtoken import views as tokenViews

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('posts', views.UserPostViewSet)
router.register('groups', views.UserGroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
  path('api/', include(router.urls)),
  path('api/login/', tokenViews.obtain_auth_token),
  path('api/logout/', views.TokenLogout.as_view()),
  path('api/users/<int:pk>/friends/', views.GetUserFriends.as_view()),
  path('api/users/<int:pk>/posts/', views.GetUserPosts.as_view()),
  path('api/users/<int:pk>/messages/', views.GetFriendMessages.as_view()),
  path('api/groups/<int:pk>/members/', views.GetGroupMembers.as_view()),
  path('api/groups/<int:pk>/messages/', views.GetGroupMessages.as_view()),
  path('api/groups/<int:pk>/requests/', views.GetGroupRequests.as_view()),
  path('api/groups/<int:pk>/magerqst/', views.ManageJoinRequest.as_view()),
  path('api/groups/<int:pk>/magerole/', views.ManageMemberRole.as_view()),
  path('admin/', admin.site.urls),
  path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]