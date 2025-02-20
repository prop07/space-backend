from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('api/space', views.space, name='space'),
    path('api/space/<str:id>', views.field, name='field'),
    path('api/view', views.view, name='view'),
]