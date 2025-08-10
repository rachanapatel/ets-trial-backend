from django.shortcuts import render
from api.serializers import ShiftSerializer, PositionSerializer, EmployeeSerializer, CreateCompanySerializer, CreateManagerSerializer, CreateNewCompanyWithManagerSerializer
from api.serializers import ManagerSerializer, CompanySerializer, PositionSerializer, CreatePositionSerializer, PlainManagerSerializer, ReadManagerSerializer
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from api.models import Shift, Position, Employee, Company
from rest_framework.decorators import api_view



class ShiftViewSet(viewsets.ModelViewSet):
    # queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    
    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        if company_id:
            return Shift.objects.filter(position__company_id=company_id)
        return Shift.objects.none()    

# class PositionsListView(generics.ListCreateAPIView):
#     queryset = Position.objects.all()
#     serializer_class = PositionSerializer 
class PositionsListCreateView(generics.ListCreateAPIView):
    serializer_class = PositionSerializer
    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        if company_id:
            return Position.objects.filter(company_id=company_id)
        return Position.objects.none()

class PositionsCreateView(generics.CreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer 
    # def perform_create(self, serializer):
    #     company = self.request.employee.company  
    #     serializer.save(company=company)       

class PositionsDetailView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer  

class EmployeesCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer    


class EmployeesListCreateView(generics.ListCreateAPIView):
    serializer_class = EmployeeSerializer
    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        if company_id:
            return Employee.objects.filter(company_id=company_id)
        return Employee.objects.none()

class EmployeesDetailView(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer    

class TeamListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    
class NewCompanyCreateView(generics.CreateAPIView, generics.ListAPIView):
    # queryset = Company.objects.all()
    queryset = Company.objects.none() 
    serializer_class = CreateCompanySerializer 
    
    def create(self, request, *args, **kwargs):
        # Step 1: Validate incoming data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company_name = serializer.validated_data['name']
        manager_name = serializer.validated_data['manager_name']
        manager_username = serializer.validated_data['manager_username']
        manager_password = serializer.validated_data.get('manager_password', '')

        # Step 2: Create related objects
        company = Company.objects.create(name=company_name)
        position = Position.objects.create(title='Manager', company=company)  
        manager = Employee.objects.create(name=manager_name, 
                                          username=manager_username, 
                                          password=manager_password, 
                                          company=company,
                                          position=position)

        # Step 3: Return full nested response
        first_response_serializer = CompanySerializer(company)
        second_response_serializer = PlainManagerSerializer(manager)
        third_response_serializer = PositionSerializer(position)

        return Response({"company": first_response_serializer.data,
                         "employee": second_response_serializer.data, 
                         "position": third_response_serializer.data},
                         status=201)
    
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    print(f"Login attempt: {username=} {password=}")

    if not username or not password:
        return Response({"detail": "Username and password are required."}, status=400)

    try:
        user = Employee.objects.get(username=username)
        print(f"Found user: {user.username=} {user.password=}")


        if user.password == password:  
            serializer = ReadManagerSerializer(user)
            return Response(serializer.data, status=200)

        return Response({"detail": "Incorrect password."}, status=401)

    except Employee.DoesNotExist:
        return Response({"detail": "User not found."}, status=401)
    
    except Exception as e:
        print("Unexpected error:", str(e))
        return Response({"detail": "Server error"}, status=500)