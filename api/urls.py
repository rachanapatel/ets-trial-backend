from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShiftViewSet, RolesCreateView, RolesDetailView, EmployeesCreateView, EmployeesDetailView, TeamListView

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'dash', ShiftViewSet, basename='shifts')

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('team/roles', RolesCreateView.as_view(), name='roles'),
    path('team/roles/<int:pk>', RolesDetailView.as_view(), name='roles-detail'),
    path('team/employees', EmployeesCreateView.as_view(), name='employees'),
    path('team/employees/<int:pk>', EmployeesDetailView.as_view(), name='employees-detail'),
    path('team', TeamListView.as_view(), name='team'),
]
