from django.urls import path

from user import views

# for the tests (to be found with reverse lookup function)
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),

]
