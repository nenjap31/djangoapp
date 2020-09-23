from django.urls import include, path
from . import views

urlpatterns = [
    path('accounts/', views.AccountList.as_view()),
    path('accounts/<int:pk>/', views.AccountDetail.as_view()),
]