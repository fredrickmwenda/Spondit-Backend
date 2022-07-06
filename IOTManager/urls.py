from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView, TokenVerifyView)
from accounts import views

urlpatterns = [
    path('',views.login_view, name="login"),
    path('admin/', admin.site.urls),
    #make login from accounts app as home page
    path("", include("accounts.urls")),
    path("", include("devices.urls")),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password/password_reset_complete.html'), name='password_reset_complete'), 

    # path("", include("notifications.urls"))
    #api token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
