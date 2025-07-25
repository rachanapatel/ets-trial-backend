from django.shortcuts import render
from api.serializers import ShiftSerializer, PositionSerializer, EmployeeSerializer, CreateCompanySerializer, CreateManagerSerializer
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from api.models import Shift, Position, Employee, Company
# Create your views here.

class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer

class PositionsCreateView(generics.CreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer    

class PositionsDetailView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer  

class EmployeesCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer    

class EmployeesDetailView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer    

class TeamListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

# class NewCompanyCreateView(generics.CreateAPIView):
#     queryset = CreateCompanySerializer.objects.all()
#     serializer_class = CreateCompanySerializer  

#     def perform_create(self, company_serializer):

#         manager_data = {
#             'name': self.request.data.get('manager_name'),
#             'username': self.request.data.get('manager_username'),
#             'password': self.request.data.get('manager_password'),
#             'is_manager': True
#         }

#         manager_serializer = CreateManagerSerializer(data=manager_data)
#         if manager_serializer.is_valid():
#             manager = manager_serializer.save()

#             company_data = {
#             'name': self.request.data.get('company_name'),
#             'manager': manager
#             }

#             company_serializer = CreateCompanySerializer(data=company_data)
#             if company_serializer.is_valid():
#                 company_serializer.save()

#                 return Response(
#                     {**company_serializer.data,
#                     'manager': manager_serializer.data}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(manager_serializer.errors, status=status.HTTP_400_BAD_REQUEST)