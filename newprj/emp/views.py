from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.db.models import Q

from .models import Employees, Salaries, Departments, DeptEmp, TITLES_ENUM, Title


@csrf_exempt
def employee_hire(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            emp_obj             = Employees()
            emp_obj.emp_no      = data['employee_id']
            emp_obj.birth_date  = data['birth_date']
            emp_obj.first_name  = data['first_name']
            emp_obj.gender      = data['gender']
            emp_obj.hire_date   = data['hire_date']
            emp_obj.clean_fields()
            emp_obj.clean()
            emp_obj.validate_unique()
            emp_obj.save()
            salary_obj            = Salaries()
            salary_obj.salary     = data['salary']['amount']
            salary_obj.from_date  = data['salary']['from_date']
            salary_obj.to_date    = data['salary']['to_date']
            salary_obj.emp        = emp_obj
            salary_obj.clean_fields()
            salary_obj.clean()
            salary_obj.validate_unique()
            salary_obj.save()
            dept_obj          = Departments.objects.get(dept_no=data['department'])
            dept_emp_obj      = DeptEmp()
            dept_emp_obj.dept = dept_obj
            dept_emp_obj.emp  = emp_obj
            dept_emp_obj.save()
            title_obj            = Title()
            title_obj.title      = data['title']['title']
            title_obj.from_date  = data['title']['from_date']
            title_obj.to_date    = data['title']['to_date']
            title_obj.emp        = emp_obj
            title_obj.clean_fields()
            title_obj.clean()
            title_obj.validate_unique()
            title_obj.save()

            return JsonResponse({
                'status': 'success', 
                'message': 'Data saved successfully'})
        except ValidationError as e:
            return JsonResponse({
                'status': 'failed', 
                'message': '',
                'errors':dict(e)})
        except IntegrityError as e:
            return JsonResponse({
                'status': 'failed', 
                'message': 'Email or phone number is Alredy exist'})
    else:
        return not_implimented
    print('123')
    return HttpResponse('123')


@csrf_exempt
def eligible_for_hike(request,emp_id):
    incl_depts = ['Customer Service', 'Development', 'Finance', 'Human Resources', 'Human Resources', 'Sales']
    incl_title = ['Senior Engineer', 'Staff', 'Engineer', 'Senior Staff', 'Assistant Engineer', 'Technique Leader']

    emp_obj = Employees.objects.get(emp_no = emp_id)
    experiance = emp_obj.hire_date.today().year - emp_obj.hire_date.year
    age = emp_obj.birth_date.today().year - emp_obj.birth_date.year
    emp_departments = emp_obj.deptemp_set.all()
    if not ((age <= 20) or (experiance <= 1)):
        for emp_dept in emp_departments:
            if emp_dept.dept.dept_name in incl_depts:
                title_obj = Title.objects.get(emp=emp_obj)
                if title_obj.title in incl_title:
                    if not (title_obj.title == "Technique Leader" and emp_obj.gender == "M"):
                        salary_obj = Salaries.objects.get(emp=emp_obj)
                        salary_obj.salary += (salary_obj.salary - 10//100)
                        title_obj.title = get_promotion(get_promotion(title_obj.title))
                        salary_obj.save()
                        title_obj.save()
                        return JsonResponse({'hike': True,'designation':title_obj.title})
                        
                        
    return JsonResponse({'hike': False})



def not_implimented():
    return JsonResponse({
                'status': 'failed', 
                'message': 'This method not implimented yet'})

def get_promotion(title):
    for key,value in TITLES_ENUM:
        if key == title:
            return value + 1
        elif value == title:
            return key