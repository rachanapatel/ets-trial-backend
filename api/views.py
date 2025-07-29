from django.shortcuts import render
from api.serializers import ShiftSerializer, PositionSerializer, EmployeeSerializer, CreateCompanySerializer, CreateManagerSerializer, CreateNewCompanyWithManagerSerializer
from api.serializers import ManagerSerializer, CompanySerializer, PositionSerializer, CreatePositionSerializer, PlainManagerSerializer
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

# class NewCompanyCreateView(generics.CreateAPIView, generics.ListAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CreateNewCompanyWithManagerSerializer  

#     # def get_serializer_class(self):
#     #     if self.request.method == 'POST':
#     #         return CreateNewCompanyWithManagerSerializer
#     #     return CompanySerializer    
    
    
#     def perform_create(self, company_serializer):

#         manager_data = {
#             'name': self.request.data.get('manager_name'),
#             'username': self.request.data.get('manager_username'),
#             'password': self.request.data.get('manager_password'),
#             'is_manager': True
#         }

#         manager_serializer = CreateManagerSerializer(data=manager_data)
#         if not manager_serializer.is_valid():
#             return Response(manager_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            

#         company_data = {
#         'name': self.request.data.get('company_name'),
#         'manager': None
#         }

#         company_serializer = CreateCompanySerializer(data=company_data)
        
#         if not company_serializer.is_valid():
#             return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         company = company_serializer.save()
#         # company = company_serializer.save(manager=manager_data)
#         total_company_serializer = CompanySerializer(company)

#         position_data = {
#         'title': "Owner/Manager",
#         'company' : total_company_serializer.data["id"]
#         }
#         # manager_position = Position(title="Owner/Manager", company=)
#         position_of_manager = CreatePositionSerializer(data=position_data)


#         # manager.company = company
#         # manager.save()
#         # manager = manager_serializer.save(company=company_data)

#         manager = manager_serializer.save(position=position_of_manager)
#         total_manager_serializer = ManagerSerializer(manager)
        

#         return Response(
#             {**total_company_serializer.data,
#             'manager': total_manager_serializer.data}, status=status.HTTP_201_CREATED)
    
    
class NewCompanyCreateView(generics.CreateAPIView, generics.ListAPIView):
    # queryset = Company.objects.all()
    queryset = Company.objects.none() 
    serializer_class = CreateCompanySerializer 
    
    
    def create(self, request, *args, **kwargs):
        # # Use the default creation logic
        # response = super().create(request, *args, **kwargs)

        # # Use a different serializer for the output
        # article = self.get_object()
        # output_serializer = ArticleReadSerializer(article)
        # return Response(output_serializer.data, status=response.status_code)


        # Step 1: Validate incoming data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company_name = serializer.validated_data['name']
        # manager_data = serializer.validated_data['company_manager']
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