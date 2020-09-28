from django.urls import include, path
from . import views


urlpatterns = [
    path('partners/', views.PartnerList.as_view()),
    path('partners/<int:pk>/', views.PartnerDetail.as_view()),
    path('rajaongkir/', views.GetRajaongkir.as_view()),
]