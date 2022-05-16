from django.contrib import admin
from django.urls import include, path


from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView, TokenVerifyView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("devices.urls")),
    # path("", include("notifications.urls"))
    #api token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
