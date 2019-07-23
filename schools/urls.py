from django.urls import path
from schools import views
urlpatterns = [
    path('', views.index),
    path('about', views.about),
    path('api/school/<int:eid>', views.school),
    path('api/school/compare', views.compare_school)
]
