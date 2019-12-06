
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# import datetime


def validate_age(value):
    year = value.today().year
    born = value.year
    age = year-born
    if age not in range(18,61):
        raise ValidationError(
            _('%(value)s given age is not between 18 to 60'),
            params={'value': age},
        )

def validate_hire_date(value):
    if value.year < 2015:
        raise ValidationError(
            _('Company is created in 2015 given year %(value)s is not a valid date'),
            params={'value': value.year},
        )