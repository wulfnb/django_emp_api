from django.db import models
from .validators import validate_age, validate_hire_date

GENDER_ENUM = [
    ('M','Male'),
    ('F','Female')
]


TITLES_ENUM = [
    ('Staff',1),
    ('Senior staff',2),
    ('Assistant Engineer',3),
    ('Engineer',4),
    ('Senior Engineer',5),
    ('Technique Lead',6),
    ('Manger',7),
]

class Employees(models.Model):
    emp_no      = models.IntegerField(unique=True,primary_key=True)
    birth_date  = models.DateField(validators=[validate_age])
    first_name  = models.CharField(max_length=16)
    gender      = models.CharField(max_length=1,choices=GENDER_ENUM)
    hire_date   = models.DateField(validators=[validate_hire_date])


class Departments(models.Model):
    dept_no     = models.CharField(unique=True,max_length=10,primary_key=True)
    dept_name   = models.CharField(max_length=40)

class DeptEmp(models.Model):
    emp     = models.ForeignKey(Employees,on_delete=models.CASCADE)
    dept    = models.ForeignKey(Departments,on_delete=models.CASCADE)

class Title(models.Model):
    emp         = models.ForeignKey(Employees,on_delete=models.CASCADE)
    title       = models.CharField(max_length=50,choices=TITLES_ENUM)
    from_date   = models.DateField(validators=[validate_hire_date])
    to_date     = models.DateField(validators=[validate_hire_date])

class Salaries(models.Model):
    emp         = models.ForeignKey(Employees,on_delete=models.CASCADE)
    salary      = models.IntegerField()
    from_date   = models.DateField(validators=[validate_hire_date])
    to_date     = models.DateField(validators=[validate_hire_date])
