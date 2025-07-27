from django.db import models
# from django.contrib.auth import User, AbstractUser

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=100)

    # manager = models.CharField(max_length=100, blank=True, default='')
    manager = models.OneToOneField('Employee', related_name='manager', on_delete=models.CASCADE, limit_choices_to={'is_manager': True}, null=True) 


class Position(models.Model):
    title = models.CharField(max_length=100)

    company = models.ForeignKey(Company, related_name='positions', on_delete=models.CASCADE)


class Employee(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20, blank=True, default='')
    contact = models.EmailField(max_length=100, blank=True, default='')
    is_manager = models.BooleanField(default=False)

    position = models.ForeignKey(Position, related_name='employees', on_delete=models.PROTECT) 
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE) 

    def is_manager(self):
        return self.is_manager
    
    
class Shift(models.Model):
    shift_status_options = {"prop": "Proposed", 
                      "acc": "Accepted", 
                      "pref": "Preferred", 
                      "rej" : "Rejected"}
    duration = models.DurationField()
    starttime = models.DateTimeField()
    status = models.CharField(choices=shift_status_options, default="prop")
    recurring = models.BooleanField(default=False)
# deleting a position deletes associated shifts BUT deleting an employee just sets the employee to null (bc its optional)
    employee = models.ForeignKey(Employee, related_name='shifts', on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey(Position, related_name='shifts', on_delete=models.CASCADE) 
