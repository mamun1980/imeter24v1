from django.contrib.admin import FieldListFilter
from django.db.models import Max, Min

class ExtraListFilter(FieldListFilter):
    pass

class NumericFieldListFilter(ExtraListFilter):
    template = "adminextra/numeric_filter.html"

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kw_min = "%s__gte" % field_path
        self.lookup_kw_max = "%s__lte" % field_path
        aggregate = model.objects.aggregate(Min(field_path), Max(field_path))
        self.model_min = model_min = aggregate["%s__min" % field_path]
        self.model_max = model_max = aggregate["%s__max" % field_path]
        self.lookup_val_min = request.GET.get(self.lookup_kw_min, model_min)
        self.lookup_val_max = request.GET.get(self.lookup_kw_max, model_max)
        super(NumericFieldListFilter, self).__init__(
            field, request, params, model, model_admin, field_path)
        self.field_name = field_path.split(".")[-1]
        self.choices_values = None

    def expected_parameters(self):
        return [self.lookup_kw_min, self.lookup_kw_max]

    def choices(self, changelist=None):
        return []
        [
            {
                'selected': True,
                'query_string': changelist.get_query_string({}, []),
                'display': "All",
            },
            {
                'selected': False,
                'query_string': changelist.get_query_string({
                    self.lookup_kw_min: self.lookup_val_min
                }, [self.lookup_kw_max]),
                'display':"Minimum"
            },
            {
                'selected': False,
                'query_string': changelist.get_query_string({
                    self.lookup_kw_max: self.lookup_val_max
                }, [self.lookup_kw_min]),
                'display':"Maximum"
            },
        ]

