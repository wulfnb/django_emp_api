
from django.urls import path
from .views import employee_hire, eligible_for_hike

urlpatterns = [
    path('employee_hire/', employee_hire,name='employee_hire'),
    path('eligible_for_hike/<int:emp_id>', eligible_for_hike,name='eligible_for_hike'),
]
