from django.shortcuts import render
from api.serializers import ShiftSerializer, RoleSerializer, EmployeeSerializer, CompanySerializer
from rest_framework import viewsets, generics
from api.models import Shift, Role, Employee, Company
# Create your views here.

class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer

class RolesCreateView(generics.CreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer    

class RolesDetailView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer  

class EmployeesCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer    

class EmployeesDetailView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer    

class TeamListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer