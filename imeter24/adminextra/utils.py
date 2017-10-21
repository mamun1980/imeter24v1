from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

def search_with_fk(lst, deep=False):
    """ Return a list of the form ["field", ("FK", [field]), "field"] into a
        list suitable for search_fields """
    def inner(l):
        for item in l:
            if isinstance(item, (list, tuple)):
                for field in item[1]:
                    if deep or not "__" in field:
                        yield "%s__%s" % (item[0], field)
            else:
                yield item
    return list(inner(lst))

def filtered_queryset(field="soldto"):
    """ Return a function for ModelAdmin get_queryset, restrictin search
        for non-superuser to models related to the user managed contact. """
    def get_queryset(self, request):
        queryset = super(self.__class__, self).get_queryset(request)
        if not request.user.is_superuser:
            filter_by_contact = {"%s__in"%field: request.user.managed.all()}
            queryset = queryset.filter(**filter_by_contact)
        return queryset
    return get_queryset

def model_to_dict(obj):
    ret = {"pk": obj.pk}
    for att in obj._meta.get_fields():
        if not hasattr(obj, att.name):
            continue
        val = getattr(obj, att.name)
        if isinstance(att, models.ForeignKey):
            if val is None:
                ret[att.name] = None
            else:
                ret[att.name] = {"str":str(val), "pk":val.pk}
        elif val.__class__.__name__ in ["RelatedManager","ManyRelatedManager"]:
            ret[att.name] =  [ {"str":str(o), "pk":o.pk} for o in val.all() ]
        else:
            ret[att.name] = val
    return ret

class ModelJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, models.Model):
            return model_to_dict(obj)
        return super(ModelJSONEncoder, self).default(obj)

def get_scores(hits, objs):
    scores = {}
    for q in hits:
        scores[q] = { h["_id"]:h["_score"] for h in hits[q]["hits"] }
    if hits.keys() == ["_"]:
        return scores["_"]
    result = {}
    for obj in objs:
        local = []
        for q in hits:
            if q == "_":
                local.append(scores.get(str(obj["pk"]), 0))
            else:
                local.append(scores.get(str(obj[q]["pk"]), 0))
        result[str(obj["pk"])] = max(local)
    return result
