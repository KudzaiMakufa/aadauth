from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.urls import path
from home import views
from django.urls import reverse_lazy

app_name = 'home'

# urlpatterns = [ 
#     url('', views.home_login , name="login"),
#     url('logout', views.home_logout, name="logout"),
#     # url('profile', views.home_profile, name="profile"),
#     # path('change-password/', auth_views.PasswordChangeView.as_view()),
#     # url('change-password/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('home:profile')), name='change_password'),
# ]

urlpatterns = [ 
    path('', views.home_login , name="login"),
    path('logout', views.home_logout, name="logout"),
#   path('profile', views.home_profile, name="profile"),
#   path('change-password/', auth_views.PasswordChangeView.as_view()),
#   path('change-password/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('home:profile')), name='change_password'),
]
