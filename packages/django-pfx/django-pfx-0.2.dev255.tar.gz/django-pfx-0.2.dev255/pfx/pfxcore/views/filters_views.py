from functools import reduce

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from pfx.pfxcore.shortcuts import (
    parse_bool,
    parse_date,
    parse_float,
    parse_int,
)
from pfx.pfxcore.views import FieldType


class FilterGroup():
    def __init__(self, name, label, filters):
        self.name = name
        self.label = label
        self.filters = filters

    @property
    def meta(self):
        return dict(is_group=True, name=self.name, label=self.label, items=[
            f.meta for f in self.filters
        ])

    def query(self, params):
        return Q(*[f.query(params) for f in self.filters])


class Filter():
    def __init__(
            self, name, label, type=None, filter_func=None,
            filter_func_list=False, choices=None,
            related_model=None):
        self.name = name
        self.label = label
        self.type = type
        self.filter_func = filter_func
        self.filter_func_list = filter_func_list
        self.choices = choices
        self.related_model = related_model

    @property
    def meta(self):
        res = dict(
            label=_(self.label),
            name=self.name,
            type=self.type)
        if self.choices:
            res['choices'] = [
                dict(label=_(v), value=k) for k, v in self.choices]
        if self.related_model:
            res['related_model'] = self.related_model
        return res

    def _parse_value(self, value):
        if self.type == FieldType.BooleanField:
            return parse_bool(value)
        if self.type in (FieldType.IntegerField, FieldType.ModelObject):
            return parse_int(value)
        if self.type == FieldType.FloatField:
            return parse_float(value)
        if self.type == FieldType.DateField:
            return parse_date(value)
        return value

    def _call_filter_func(self, values):
        if self.filter_func_list:
            return self.filter_func(values)
        return reduce(
            lambda x, y: x | y, [self.filter_func(v) for v in values])

    def query(self, params):
        values = [self._parse_value(v) for v in params.getlist(self.name)]
        return self._call_filter_func(values) if values else Q()


class ModelFilter(Filter):
    def __init__(
            self, model, name, label=None, type=None, filter_func=None,
            filter_func_list=False, choices=None, related_model=None):
        self.model = model
        self.field = model._meta.get_field(name)
        super().__init__(
            name, label or self.field.verbose_name,
            type or FieldType.from_model_field(self.field.__class__),
            filter_func, filter_func_list, choices or self.field.choices,
            related_model or (
                self.field.remote_field and
                self.field.remote_field.model.__name__))

    @property
    def meta(self):
        res = dict(
            is_group=False, label=_(self.label), name=self.name,
            type=self.type)
        if self.choices:
            res['choices'] = [
                dict(label=_(v), value=k) for k, v in self.choices]
        if self.related_model:
            res['related_model'] = self.related_model
        return res

    def query(self, params):
        values = [self._parse_value(v) for v in params.getlist(self.name)]
        if self.filter_func and values:
            return self._call_filter_func(values)
        elif values:
            return reduce(
                lambda x, y: x | y, [Q(**{self.name: v}) for v in values])
        return Q()
