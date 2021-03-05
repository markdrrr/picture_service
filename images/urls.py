from django.urls import path

from images.views import ListImage, view_image, add_image

urlpatterns = [
    path('', ListImage.as_view(), name='home'),
    path('image/<int:pk>/', view_image, name='view_image'),
    path('add/', add_image, name='add_image'),
]
