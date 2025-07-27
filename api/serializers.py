from rest_framework import serializers
from api.models import Company, Shift, Employee, Position

# class CompanySerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)

#     name = models.CharField(max_length=100)
#     manager = models.CharField(max_length=100, blank=True, default='')
#     employees = models.
#     positions  

class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']

class CreateManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        # fields = ['name', 'username', 'password', 'is_manager']
        fields = '__all__'

class PlainManagerSerializer(serializers.ModelSerializer):
    # company = CompanySerializer

    class Meta:
        model = Employee
        fields = ['id', 'name', 'is_manager', 'username', 'password','company']

class CompanySerializer(serializers.ModelSerializer):
    manager = PlainManagerSerializer
    class Meta:
        model = Company
        fields = ['id', 'name', 'manager']

class ManagerSerializer(serializers.ModelSerializer):
    company = CompanySerializer

    class Meta:
        model = Employee
        fields = ['id', 'name', 'is_manager', 'username', 'password','company']


class CreateNewCompanyWithManagerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    manager = CreateManagerSerializer()

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'
        
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'