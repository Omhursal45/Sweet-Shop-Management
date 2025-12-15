from django.urls import path
from .views import RegisterView, LoginView, protected_view

# Make JWT refresh view optional
try:
    from rest_framework_simplejwt.views import TokenRefreshView
    urlpatterns = [
        path('register/', RegisterView.as_view(), name='register'),
        path('login/', LoginView.as_view(), name='login'),
        path('protected/', protected_view, name='protected'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]
except ImportError:
    # JWT not available, skip token refresh endpoint
    urlpatterns = [
        path('register/', RegisterView.as_view(), name='register'),
        path('login/', LoginView.as_view(), name='login'),
        path('protected/', protected_view, name='protected'),
    ]
