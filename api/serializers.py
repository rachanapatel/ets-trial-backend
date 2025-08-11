from rest_framework import serializers
from api.models import Company, Shift, Employee, Position



class CreateCompanySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    manager_name = serializers.CharField(max_length=100)
    manager_username = serializers.CharField(max_length=20)
    manager_password = serializers.CharField(max_length=20, required=False, allow_blank=True, default='')

class CreatePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['title']

class CreateManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name', 'username', 'password']


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'title', 'company']

class PlainManagerSerializer(serializers.ModelSerializer):
    position = PositionSerializer
    is_manager = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'name', 'username', 'password', 'contact', 'position', 'is_manager']
    
    def is_manager(self, obj):
        return obj.is_manager()


class CompanySerializer(serializers.ModelSerializer):
    employees = PlainManagerSerializer
  
    class Meta:
        model = Company
        fields = ['id', 'name', 'employees']

class ManagerSerializer(serializers.ModelSerializer):
    company = CompanySerializer
    position = PositionSerializer

    class Meta:
        model = Employee
        fields = ['id', 'name', 'username', 'password', 'contact', 'position','company']


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

class EmployeeSerializer(serializers.ModelSerializer):
    position = PositionSerializer(read_only=True) 
    position_id = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(), source='position', write_only=True)
    company = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'contact', 'position', 'position_id', 'company']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['username'] = instance.username
        return data

class ReadManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'username', 'position', 'company']