from django.urls import path
from . import views

urlpatterns = [
    path('buy/<int:id>/', views.CreateCheckoutSessionView.as_view(), name='buy'),
    path('item/<int:id>/', views.item_detail, name='item'),
    path('success/', views.success_page, name='success_page'),
    path('cancel/', views.cancel_page, name='cancel_page'),
]