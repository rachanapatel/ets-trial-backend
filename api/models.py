from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=100)

    manager = models.CharField(max_length=100, blank=True, default='')


class Role(models.Model):
    title = models.CharField(max_length=100)

    company = models.ForeignKey(Company, related_name='roles', on_delete=models.CASCADE)


class Employee(models.Model):
    name = models.CharField(max_length=100)
    contact = models.EmailField(max_length=100, blank=True, default='')
    is_manager = models.BooleanField(default=False)

    role = models.ForeignKey(Role, related_name='employees', on_delete=models.PROTECT)
    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    
    
class Shift(models.Model):
    shift_status_options = {"prop": "Proposed", 
                      "acc": "Accepted", 
                      "pref": "Preferred", 
                      "rej" : "Rejected"}
    duration = models.DurationField()
    starttime = models.DateTimeField()
    status = models.CharField(choices=shift_status_options, default="prop")
    recurring = models.BooleanField(default=False)
# deleting a role deletes assocaited shifts BUT deleting an employee just sets the employee to null (bc its optional)
    employee = models.ForeignKey(Employee, related_name='shifts', on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey(Role, related_name='shifts', on_delete=models.CASCADE)