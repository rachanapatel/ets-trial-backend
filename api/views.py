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

class PositionsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer  

class EmployeesCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer    

def generate_username(employee_name):
    base_username = ''.join(employee_name.split()).lower()  
    if Employee.objects.filter(username=base_username).exists(): 
        counter = 1
        new_username = f"{base_username}{counter}"
        while Employee.objects.filter(username=new_username).exists(): 
            counter += 1
            new_username = f"{base_username}{counter}"
        return new_username
    return base_username

class EmployeesListCreateView(generics.ListCreateAPIView):
    serializer_class = EmployeeSerializer
    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        if company_id:
            return Employee.objects.filter(company_id=company_id)
        return Employee.objects.none()
    def perform_create(self, serializer):
        company_id = self.request.headers.get('X-Company-ID')
        if company_id:
            company = Company.objects.get(id=company_id)

        employee_name = serializer.validated_data['name']
        username = generate_username(employee_name)
        password = username
        serializer.save(username=username, company=company)     
        employee = serializer.save(username=username, password=password)
        employee.save()   


class EmployeesDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeSerializer    
    def get_queryset(self):
        company_id = self.request.headers.get('X-Company-ID')
        if company_id:
            return Employee.objects.filter(company_id=company_id)
        return Employee.objects.none()

class TeamListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    
class NewCompanyCreateView(generics.CreateAPIView, generics.ListAPIView):
    # queryset = Company.objects.all()
    queryset = Company.objects.none() 
    serializer_class = CreateCompanySerializer 
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company_name = serializer.validated_data['name']
        manager_name = serializer.validated_data['manager_name']
        manager_username = serializer.validated_data['manager_username']
        manager_password = serializer.validated_data.get('manager_password', '')

        company = Company.objects.create(name=company_name)
        position = Position.objects.create(title='Manager', company=company)  
        manager = Employee.objects.create(name=manager_name, 
                                          username=manager_username, 
                                          password=manager_password, 
                                          company=company,
                                          position=position)

        first_response_serializer = CompanySerializer(company)
        second_response_serializer = PlainManagerSerializer(manager)
        third_response_serializer = PositionSerializer(position)

        return Response({"company": first_response_serializer.data,
                         "employee": second_response_serializer.data, 
                         "position": third_response_serializer.data},
                         status=201)
    
@api_view(['POST'])
def login_view(request):
    # if request.method == 'POST':

    username = request.data.get('username')
    password = request.data.get('password')

    print(f"Login attempt: {username=} {password=}")

    if not username or not password:
        return Response({"detail": "Username and password are required."}, status=400)

    try:
        user = Employee.objects.get(username=username)
        print(f"Found user: {user.username=} {user.password=}")


        if user.password == password:  
            position_title = user.position.title  
            serializer = ReadManagerSerializer(user)
            return Response({
                **serializer.data,
                "is_manager": position_title == "Manager",  
                "position": position_title 
            }, status=200)

        return Response({"detail": "Incorrect password."}, status=401)

    except Employee.DoesNotExist:
        return Response({"detail": "User not found."}, status=401)
    
    except Exception as e:
        print("Unexpected error:", str(e))
        return Response({"detail": "Server error"}, status=500)

    # elif request.method == 'GET':
    #     return Response({"message": "Please provide your credentials to login."}, status=status.HTTP_200_OK)
