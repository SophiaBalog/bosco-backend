import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_product_year(value):
    current_year = datetime.date.today().year
    if value.year > current_year:
        raise ValidationError(
            _("Рік випуску не може бути з майбутнього (максимум %(max_year)s)."),
            code='invalid_year',
            params={'max_year': current_year},
        )