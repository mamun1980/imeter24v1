from collections import OrderedDict
from functools import update_wrapper
import json
import logging
from time import time

logger = logging.getLogger(__name__)

from django.apps import apps
from django.conf import settings
from django.conf.urls import url
from django.contrib.admin import AdminSite
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.core import serializers
from django.db.models import Q
from django.db.models.base import ModelBase
from django.db.models.signals import post_save, post_delete
from django.http.response import JsonResponse, HttpResponse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

import elasticsearch

import utils
from .filters import ExtraListFilter

ES_SERVER = getattr(settings, 'ELASTICSEARCH_SERVER', None)
ES_RESULT = getattr(settings, 'ELASTICSEARCH_RESULT', 20)
if ES_SERVER:
    _es = elasticsearch.Elasticsearch(hosts=ES_SERVER)
else:
    _es = None

FIELD_TO_TYPE = {
    "AutoField": "integer",
    "BigIntegerField": "long",
    "BooleanField": "boolean",
    "CharField": "string",
    "DateField": "date",
    "DateTimeField": "date",
    "DecimalField": "double",
    "DurationField": "long",
    "EmailField": "string",
    "FloatField": "float",
    "IntegerField": "integer",
    "GenericIPAddressField": "string",
    "PositiveIntegerField": "integer",
    "PositiveSmallIntegerField": "short",
    "SlugField": "string",
    "SmallIntegerField": "short",
    "TextField": "string",
    "URLField": "string",
    "UUIDField": "string",
}
FIELD_TO_FORMAT = {
    "DateField": "date_optional_time",
    "DateTimeField": "date_time_no_millis",
}


class AdminSiteWithOps(AdminSite):
    index_template = "adminextra/index.html"

    def __init__(self, *args, **kwargs):
        super(AdminSiteWithOps, self).__init__(*args, **kwargs)
        assert isinstance(self._registry, dict)
        self._actions = OrderedDict(self._actions)
        k, v = self._actions.popitem()
        self._actions['index_selected'] = self._index_selected
        self._actions[k] = v
        self.ops = {}
        self.reorder_inlines = []
        self.indexed_fields = {}
        self.indexed_models = []

    def index(self, request, extra_context=None):
        """
        Displays the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        # import pdb; pdb.set_trace();
        if request.user.is_authenticated() and request.user.username != 'admin':
            return HttpResponseRedirect("/user/dashboard")

        app_list = self.get_app_list(request)

        context = dict(
            self.each_context(request),
            title=self.index_title,
            app_list=app_list
        )
        context.update(extra_context or {})

        request.current_app = self.name

        return TemplateResponse(request, self.index_template or 'admin/index.html', context)

    def _index(self, item):
        """ index in elasticsearch one object """
        info = item._meta.app_label.lower(), item._meta.model_name.lower()
        search, display = self.indexed_fields.get("%s_%s" % info, (None, None))
        fields = set(search).union(display)
        itm = {}
        for f in fields:
            att = getattr(item, f.strip("=^@"), None)
            if att is None:
                continue
            if hasattr(att, "isoformat"):
                att = att.isoformat()
            itm[f] = att
        _es.index(index="%s.%s" % info, doc_type="model", id=item.pk, body=itm)

    def _index_bulk(self, queryset):
        """ index in elasticsearch all object from a queryset """
        start = inter = time()
        total = queryset.count()
        if total == 0:
            return True
        for i, obj in enumerate(queryset):
            self._index(obj)
            if 10 < time() - inter:
                # every 10 seconds, print status
                inter = time()
                eta = int((total - i) * ((inter - start) / i))
                if eta < 2:
                    # don't print ETA in the last 2 seconds
                    continue
                print("%s/%s objects indexed. ETA: %ss" % (i, total, eta))
        print("Indexed %s objects in %ss" % (total, time() - start))
        return True


    def _index_selected(self, modeladmin, request, queryset):
        """ admin action, index a list of selected object """
        opts = modeladmin.model._meta
        info = opts.app_label.lower(), opts.model_name.lower()
        search = self.indexed_fields.get("%s_%s" % info, None)
        if search == None:
            messages.warning(request, "%s%s" % (
                "You can't index object of type %s. " % info[1],
                "Please check your configuration."))
            return
        if self._index_bulk(queryset):
            messages.success(request,
                "%s objects have been indexed successfully." %queryset.count())
        else:
            messages.error(request, "An error happened while indexing")
    _index_selected.short_description ="Index selected %(verbose_name_plural)s"

    def _on_save(self, sender, **kwargs):
        """ signal action, index a created or updated object """
        self._index(kwargs["instance"])

    def _on_delete(self, sender, **kwargs):
        """ signal action, unindex deleted object """
        info = "%s.%s" % (
            sender._meta.app_label.lower(), sender._meta.model_name.lower())
        try:
            _es.delete(index=info, doc_type="model", id=kwargs["instance"].pk)
        except elasticsearch.NotFoundError:
            logger.warning("Trying to delete missing %s" % kwargs["instance"])

    def _build_mapping(self, admin_class, model):
        """ utility, build an ES mapping dict """
        fields = set(admin_class.search_fields).union(admin_class.list_display)
        filters = []
        for f in admin_class.list_filter:
            if (isinstance(f, (list, tuple))
                and issubclass(f[1], ExtraListFilter)):
                    filters.append(f[0])
        fields = fields.union(filters)
        mapping = {}
        search_fields = [f.lstrip("=^@") for f in admin_class.search_fields]
        for field in [f for f in fields if hasattr(model, f)]:
            internal_type = model._meta.get_field(field).__class__.__name__
            t = FIELD_TO_TYPE.get(internal_type, None)
            if t is None:
                msg = "%s from %s do not map (type %r)."
                raise ImproperlyConfigured(msg %
                    (field, admin_class.__name__, internal_type))
            mapping[field] = {"type": t}
            if not (field in search_fields or field in filters):
                mapping[field]["index"] = "no"
            if internal_type == "EmailField":
                mapping[field]["analyzer"] = "whitespace"
            if internal_type in FIELD_TO_FORMAT:
                mapping[field]["format"] = FIELD_TO_FORMAT[internal_type]
# The doc strongly suggest to set boost in the search query
#           if field in admin_class.search_fields:
#               sf = admin_class.search_fields
#               mapping[field]["boost"] = len(sf) - sf.index(field)
        return mapping

    def _set_or_update_mapping(self, admin_class, model):
        """ called when model register, setup a model in ES """
        app = model._meta.app_label.lower()
        model_name = model._meta.model_name.lower()
        idx = "%s.%s" % (app, model_name)
        if not _es.indices.exists(index=idx):
            _es.indices.create(index=idx)
        mappings = _es.indices.get_mapping(index=idx, doc_type="model")
        properties = self._build_mapping(admin_class, model)
        if not mappings:
            print("no mapping for %s, creating" % idx)
            mapping = {"model": {
                    "_all": {"enabled": False}, # is for query on all field
                    "properties": properties,
            }}
            _es.indices.put_mapping(index=idx, doc_type="model", body=mapping)
            return
        m_p = mappings[idx]["mappings"]["model"]["properties"]
        mapping_prop = {k:m_p[k] for k in m_p if hasattr(model, k)}
        if mapping_prop != properties:
            print("new mapping for %s" % idx)
            # delete index
            _es.indices.delete(index=idx)
            start = time()
            while _es.indices.exists(index=idx):
                from time import sleep
                sleep(0.2)
                _es.indices.delete(index=idx)
                if 10 < time() - start:
                    logger.warning("Trouble deleting mapping for %s" % idx)
            # rebuild index
            _es.indices.create(index=idx)
            mapping = {"model": {
                    "_all": {"enabled": False}, # is for query on all field
                    "properties": properties,
            }}
            _es.indices.put_mapping(index=idx, doc_type="model", body=mapping)
            # reindex
            if self._index_bulk(model.objects.all()):
                print("Successfully indexed %s" % idx)
            else:
                print("Something went wrong with %s" % idx)

    def _build_search_query(self, query_term, filters, app, model_name):
        """ Construct a query dict for elasticsearch """
        s_f, _ = self.indexed_fields[("%s_%s" % (app, model_name)).lower()]
        model = apps.get_app_config(app).get_model(model_name)
        r = {"_":{"@":[], "=":[], "^":[]}, "_order":["_"]}

        for i, field in enumerate(s_f):
            # Separate field from foreign key
            if not "__" in field:
                query = "_"
            else:
                query, field = field.split("__", 1)
                if not query in r:
                    r[query] = {"@":[], "=":[], "^":[]}
                    r["_order"].append(query)
            # build queries for full search, exact match...
            boost = len(s_f) - i
            raw_f = field.lstrip("=^@")
            if field[0] in "=^@":
                r[query][field[0]].append("%s^%s" % (raw_f, boost))
            else:
                r[query]["@"].append("%s^%s" % (raw_f, boost))

        # compute filter if required
        if filters:
            filter = { "range": {
                f[0]: {'gte':float(f[1]), 'lte':float(f[2])} for f in filters
            } }
        else:
            filter = None
        # compute the differents query
        for k, v in r.items():
            if k == "_order":
                continue
            # base query
            query = { "bool": { "should": []}}
            # full text search
            if r[k]["@"]:
                query["bool"]["should"].append({
                    "query_string": {
                        "fields": r[k]["@"],
                        "query": "*%s*" % query_term,
                        "analyze_wildcard": True,
                    }
                })
            # Start of string search
            if r[k]["^"]:
                query["bool"]["should"].append({
                    "query_string": {
                        "fields": r[k]["^"],
                        "query": "%s*" % query_term,
                        "analyze_wildcard": True,
                    }
                })
            # Exact search
            if r[k]["="]:
                for f in r[k]["="]:
                    f, b = f.split("^")
                    query["bool"]["should"].append({
                        "match": { f: {"query": query_term, "boost": b} }
                    })
            # Either simple search or search + filter
            if k == "_" and filter:
                # query with filter
                r[k] = {"size": ES_RESULT, "query": {"filtered":
                    {"query": query, "filter": filter}
                }}
            else:
                r[k] = {"size": ES_RESULT, "query": query }
        return r

    def _search(self, request, app, model_label):
        """ view, query ES, --fetch actual object-- and return json """
        # Gather search arguments
        query = request.GET.get("q", None)
        if not query:
            return JsonResponse({"hits": [], "success":False,
                    "error": "Please enter a query"})
        start = time()
        times = OrderedDict()
        filters = json.loads(request.GET.get("f", "false"))
        queries = self._build_search_query(query, filters, app, model_label)
        times["build_query"] = time() - start
        model = apps.get_app_config(app).get_model(model_label)
        # Return list of search queries if required
        if request.GET.get("raw", False):
            sub_queries = {}
            for q in queries["_order"]:
                if q == "_":
                    index = "%s.%s" % (app.lower(), model_label.lower())
                else:
                    meta = getattr(model, q).field.related_model._meta
                    a_label, m_label = meta.app_label, meta.model_name
                    index = "%s.%s" % (a_label.lower(), m_label.lower())
                sub_queries[index] = queries[q]
            return JsonResponse(sub_queries, json_dumps_params={"indent":2})
        # Do the search over all the sub-query, one main and one per FK
        objs_list = {}
        for q in queries["_order"]:
            if q == "_":
                index = "%s.%s" % (app.lower(), model_label.lower())
            else:
                meta = getattr(model, q).field.related_model._meta
                a_label, m_label = meta.app_label, meta.model_name
                index = "%s.%s" % (a_label.lower(), m_label.lower())
            objs_list[q] = _es.search(index=index, doc_type="model",
                body=queries[q])["hits"]
        times["es_queries"] = time() - start
        total = sum([objs_list[r]["total"] for r in objs_list])
        if total == 0:
            return JsonResponse({"hits": [], "success":True, "times": times})

        # Convert ES items into django item
        admin = self._registry[model]
        call_to_add = [ getattr(admin, c) for c in admin.list_display
            if not hasattr(model, c) ]

        # build a OR SQL query, using Q objects
        query = Q(pk__in = [h["_id"] for h in objs_list["_"]["hits"]])
        for k,v in {k:objs_list[k] for k in objs_list if k != "_"}.items():
            d = {"%s__pk__in" % k: [h["_id"] for h in objs_list[k]["hits"]]}
            query |= Q(**d)
        objs = model.objects.filter(query)
        times["gather_django_object"] = time() - start

        # convert result to dict
        data = []
        for obj in objs:
            o = utils.model_to_dict(obj)
            for call in call_to_add:
                o[call.__name__] = call(obj)
            data.append(o)
        times["model_to_dict"] = time() - start

        # sort result by score
        scores = utils.get_scores(objs_list, data)
        for d in data:
            d["_score"] = scores[str(d["pk"])]
        data = sorted(data, key=lambda i: i["_score"], reverse=True)
        times["sort_django_object"] = time() - start

        # Return result as JSON
        headers = { f.name:getattr(f, 'verbose_name', f.name)
            for f in model._meta.get_fields() }
        for c in call_to_add:
            headers[c.__name__] = getattr(c, "short_description",c.__name__)

        params = {}
        if not request.is_ajax():
            params["indent"] = 4
        times["total"] = time() - start
        return JsonResponse({"hits": data, "headers": headers,
            "success":True, "count": len(data), "times": times},
            encoder=utils.ModelJSONEncoder, json_dumps_params=params)

    def _fetch(self, request, app, model):
        """ Get one object and return it """
        pk = request.GET.get("pk", None)
        if not pk:
            return JsonResponse({"error": "missing pk"})
        model = apps.get_app_config(app).get_model(model)
        pk_att = model._meta.pk.attname
        obj = get_object_or_404(model, pk=pk)
        data = json.loads(serializers.serialize("json", [obj]))[0]
        data = dict(data["fields"], **{pk_att:data["pk"]})
        return JsonResponse(data)

    def each_context(self, request):
        """ Inject our own data into each admin page context data """
        context = super(AdminSiteWithOps, self).each_context(request)
        url_tag = request.resolver_match.url_name.rsplit("_", 1)[0]
        # Add information on which JS operation to run on admin forms
        if url_tag in self.ops:
            context.update({ 'ops': self.ops[url_tag] })
        # Add switch to reorder inlines fields
        if url_tag in self.reorder_inlines:
            context.update({ 'reorder_inlines': True})
        return context

    def get_urls(self):
        """ Add url endpoint for searching object """
        urlpatterns = super(AdminSiteWithOps, self).get_urls()

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            wrapper.admin_site = self
            return update_wrapper(wrapper, view)

        for (app, model) in self.indexed_models:
            urlpatterns = [
                url(r'^(?P<app>%s)/(?P<model_label>%s)/search/' % (app, model),
                    wrap(self._search), name='search_%s_%s' % (app, model) ),
                url(r'^(?P<app>%s)/(?P<model>%s)/get/' % (app, model),
                    wrap(self._fetch), name='fetch_%s_%s' % (app, model) ),
            ] + urlpatterns
        return urlpatterns

    def register(self, models, admin_cls=None, **opt):
        """ When registering model, add plenty of extra nice stuff """
        super(AdminSiteWithOps, self).register(models, admin_cls, **opt)
        if isinstance(models, ModelBase):
            models = [models]
        for model in models:
            tag = "%s_%s" % (model._meta.app_label, model._meta.model_name)
            if admin_cls and getattr(admin_cls, "reorder_inlines", False):
                self.reorder_inlines.append(tag)
                form_template = 'adminextra/change_form.html'
            if admin_cls and hasattr(admin_cls, 'adminextra_fields'):
                # Handle JS operation on fields
                self.ops[tag] = admin_cls.adminextra_fields
                form_template = 'adminextra/change_form.html'
                if admin_cls.add_form_template == None:
                    admin_cls.add_form_template = form_template
                if admin_cls.change_form_template == None:
                    admin_cls.change_form_template = form_template
            if admin_cls and _es and getattr(admin_cls, "index", False):
                # Handle ElasticSearch index
                if not hasattr(admin_cls, 'search_fields'):
                    raise ImproperlyConfigured(
                        "Can't index without search fields.")
                if not hasattr(admin_cls, 'list_display'):
                    raise ImproperlyConfigured(
                        "Can't index without list of fields to display.")
                self.indexed_fields[tag.lower()] = (
                    admin_cls.search_fields, admin_cls.list_display)
                self.indexed_models += [(
                        model._meta.app_label, model._meta.model_name
                    )]
                try:
                    self._set_or_update_mapping(admin_cls, model)
                    post_save.connect(self._on_save, sender=model)
                    post_delete.connect(self._on_delete, sender=model)
                except ImproperlyConfigured as e:
                    logger.warning("Got an improperlyConfigured error")
                    logger.warning(e)
