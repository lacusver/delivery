from typing import Any, Optional
from django.db.models import OuterRef, Subquery, PositiveIntegerField, expressions, IntegerField


class SubqueryCount(Subquery):
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = PositiveIntegerField()


class SubquerySum(Subquery):
    template = '(SELECT sum(_sum."%(column)s") FROM (%(subquery)s) _sum)'

    def __init__(self, queryset, column, output_field=PositiveIntegerField(), **extra):
        super().__init__(queryset, output_field, column=column, **extra)


class Epoch(expressions.Func):
    template = 'EXTRACT(epoch FROM %(expressions)s)::INTEGER'
    output_field = IntegerField()
