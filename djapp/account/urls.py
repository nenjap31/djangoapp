from django.urls import include, path
from . import views

urlpatterns = [
    path('accounts/', views.AccountList.as_view()),
    path('accounts/<int:pk>/', views.AccountDetail.as_view()),
    path('profile/', views.ProfileDetail.as_view()),
    path('changepassword/', views.UpdatePassword.as_view()),
    path('signup/', views.SignupUser.as_view()),
]