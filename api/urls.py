from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShiftViewSet, PositionsCreateView, PositionsDetailView, EmployeesCreateView, EmployeesDetailView, TeamListView, NewCompanyCreateView
from .views import login_view, PositionsListCreateView, EmployeesListCreateView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'dash', ShiftViewSet, basename='shifts')

# from .views import SimpleView


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    # path('team/positions/', PositionsCreateView.as_view(), name='positions'),
    path('team/positions/', PositionsListCreateView.as_view(), name='positions'),
    path('team/positions/<int:pk>/', PositionsDetailView.as_view(), name='positions-detail'),
    # path('team/employees/', EmployeesCreateView.as_view(), name='employees'),
    path('team/employees/', EmployeesListCreateView.as_view(), name='employees'),
    path('team/employees/<int:pk>/', EmployeesDetailView.as_view(), name='employees-detail'),
    path('team/', TeamListView.as_view(), name='team'),
    path('signup/', NewCompanyCreateView.as_view(), name='team'),
    path('login/', login_view),

        # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
