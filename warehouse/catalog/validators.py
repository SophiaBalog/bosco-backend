import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible



def validate_product_year(value):
    current_year = datetime.date.today().year
    if value.year > current_year:
        raise ValidationError(
            _("Рік випуску не може бути з майбутнього (максимум %(max_year)s)."),
            code='invalid_year',
            params={'max_year': current_year},
        )


def validate_article_prefix(value):
    if not value.startswith("ART-"):
        raise ValidationError(
            _("Артикул повинен починатися з префікса 'ART-'."),
            code='invalid_article_prefix'
        )

@deconstructible
class MaxWords:
    def __init__(self, limit):
        self.limit = limit

    def __call__(self, value):
        if len(value.split()) > self.limit:
            raise ValidationError(
                _("Максимальна кількість слів не повинна перевищувати %(limit)s."),
                params={"limit": self.limit},
                code="too_long"
            )

    def __eq__(self, other):
        return isinstance(other, MaxWords) and self.limit == other.limit