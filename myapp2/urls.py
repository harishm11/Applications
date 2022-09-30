
from django.urls import path
from myapp2.views import *
from myapp2.views.authenticate import *

urlpatterns = [
	path('', views.homeview.as_view(), name="home"),

	path('login/',login_view, ),
	path('logout/',logout_view),
	path('register/',register_view),
	path('password_change/',PasswordResetByUser.as_view()),

	path('feedback/',feedbackview),
]



