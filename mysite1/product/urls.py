from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index),
    path('addcomment/<int:id>',views.addcomment,name="addcommnet"),

  ]