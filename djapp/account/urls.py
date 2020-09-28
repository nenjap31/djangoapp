from django.urls import include, path
from . import views

urlpatterns = [
    path('accounts/', views.AccountList.as_view()),
    path('accounts/<int:pk>/', views.AccountDetail.as_view()),
    path('profile/', views.ProfileDetail.as_view()),
    path('changepassword/', views.UpdatePassword.as_view()),
    path('signup/', views.SignupUser.as_view()),
    path('user_group/', views.UserGroupList.as_view()),
    path('user_group/<int:pk>/', views.UserGroupDetail.as_view()),
    path('user/group/', views.GroupList.as_view()),
    path('user/group/<int:pk>/', views.GroupDetail.as_view()),
    path('user/permission/', views.PermissionList.as_view()),
    path('user/permission/<int:pk>/', views.PermissionDetail.as_view()),
]