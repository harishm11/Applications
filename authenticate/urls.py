
from django.urls import path
from authenticate.views import *
from authenticate.views.authenticate import *

urlpatterns = [
    path('', views.homeview.as_view(), name="home"),

    path('login/', login_view, ),
    path('logout/', logout_view),
    path('register/', register_view),
    path('password_change/', PasswordResetByUser.as_view()),
    path('feedback/', feedbackview),
    path('switchrole/', switch_group, name="switch_group"),
]
