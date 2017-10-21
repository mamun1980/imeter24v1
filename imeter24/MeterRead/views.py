from django.core.serializers import serialize
from django.http import JsonResponse
import json
import datetime

from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.forms.models import model_to_dict


from imeter24.Devices.models import *
from imeter24.Contacts.models import *

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()

def customer_list_json(request):
	# import pdb; pdb.set_trace();
	contacts = Contacts.objects.all().distinct("customer_name")
	serailized_contacts = serialize('json', contacts, indent=2)

	return HttpResponse(serailized_contacts, content_type="application/json")
	return JsonResponse(serailized_contacts, safe=False)



def dashboard(request):
    context = {}
    return TemplateResponse(request, 'user/dashboard.html', context)


def device_data_for_soldto(request, soldto):
	# import pdb; pdb.set_trace();
	dd_by_soldto = Devices_Data.objects.select_related("soldto").filter(soldto=soldto)[:20]
	dd_by_soldto_list = []
	for dds in dd_by_soldto:
		dds_dict = {}

		soldto = {}
		soldto['id'] = dds.soldto.accountid
		soldto['customer_name'] = dds.soldto.customer_name
		dds_dict['soldto'] = soldto

		siteid = {}
		try:
			siteid['id'] = dds.siteid.accountid
			siteid['customer_name'] = dds.siteid.customer_name
		except Exception as e:
			pass

		dds_dict['siteid'] = siteid

		dds_dict['pk'] = dds.pk
		dds_dict['locationid'] = dds.locationid
		dds_dict['device_address'] = dds.device_address
		dds_dict['device_register'] = dds.device_register
		dds_dict['data_timestamp'] = dds.data_timestamp
		dds_dict['device_read_status'] = dds.device_read_status
		dds_dict['data_timestamp'] = dds.data_timestamp

		dd_by_soldto_list.append(dds_dict)

	# import pdb; pdb.set_trace();
	# serailized_dd = serialize('json', dd_by_soldto_list, indent=2)
	serailized_dd = json.dumps(dd_by_soldto_list, default=datetime_handler)
	return HttpResponse(serailized_dd, content_type="application/json")


def locations(request, soldto, locid, regid):
	# import pdb; pdb.set_trace()

	dd_locations = Devices_Data.objects.filter(soldto=soldto, locationid=locid, device_register=regid).order_by('data_timestamp')[:20]

	ids = []
	dd_by_location_list = []

	for dds in dd_locations:
		if dds.pk not in ids:
			ids.append(dds.pk)
			dds_dict = {}

			soldto = {}
			soldto['id'] = dds.soldto.accountid
			soldto['customer_name'] = dds.soldto.customer_name
			dds_dict['soldto'] = soldto

			siteid = {}
			try:
				siteid['id'] = dds.siteid.accountid
				siteid['customer_name'] = dds.siteid.customer_name
			except Exception as e:
				pass

			dds_dict['siteid'] = siteid
			dds_dict['pk'] = dds.pk
			dds_dict['locationid'] = dds.locationid
			dds_dict['device_address'] = dds.device_address
			dds_dict['device_register'] = dds.device_register
			dds_dict['data_timestamp'] = dds.data_timestamp
			dds_dict['device_read_status'] = dds.device_read_status
			dds_dict['data_kwatts'] = dds.data_kwatts
			dds_dict['data_kva'] = dds.data_kva
			dds_dict['data_frequency'] = dds.data_frequency
			dds_dict['data_voltage_average'] = dds.data_voltage_average
			dds_dict['data_total_current'] = dds.data_total_current
			dds_dict['data_total_watts'] = dds.data_total_watts
			dds_dict['data_total_va'] = dds.data_total_va
			dds_dict['data_voltage_a'] = dds.data_voltage_a
			dds_dict['data_voltage_b'] = dds.data_voltage_b
			dds_dict['data_voltage_c'] = dds.data_voltage_c
			dds_dict['data_current_a'] = dds.data_current_a
			dds_dict['data_current_b'] = dds.data_current_b
			dds_dict['data_current_c'] = dds.data_current_c
			dds_dict['data_timestamp'] = dds.data_timestamp

			dd_by_location_list.append(dds_dict)

	serailized_dc_locations = json.dumps(dd_by_location_list, default=datetime_handler)
	return HttpResponse(serailized_dc_locations, content_type="application/json")
    # return TemplateResponse(request, 'user/locations.html', context)

def meters(request, soldto, locid, id):
	meters = Devices_Data.objects.filter(soldto=soldto, locationid=locid, id=id).order_by('data_timestamp')
	# ids = []
	# dd_by_location_list = []

	# for dds in meters:
	# 	if dds.pk not in ids:
	# 		ids.append(dds.pk)
	# 		dds_dict = {}
	#
	# 		soldto = {}
	# 		soldto['id'] = dds.soldto
	# 		soldto['customer_name'] = dds.soldto.customer_name
	# 		dds_dict['soldto'] = soldto
	#
	# 		siteid = {}
	# 		try:
	# 			siteid['id'] = dds.siteid
	# 			siteid['customer_name'] = dds.siteid.customer_name
	# 		except Exception as e:
	# 			pass
	#
	# 		dds_dict['siteid'] = siteid
	# 		dds_dict['pk'] = dds.pk
	# 		dds_dict['locationid'] = dds.locationid
	# 		dds_dict['device_address'] = dds.device_address
	# 		dds_dict['device_register'] = dds.device_register
	# 		dds_dict['data_timestamp'] = dds.data_timestamp
	# 		dds_dict['device_read_status'] = dds.device_read_status
	# 		dds_dict['data_voltage_a'] = dds.data_voltage_a
	# 		dds_dict['data_voltage_b'] = dds.data_voltage_b
	# 		dds_dict['data_voltage_c'] = dds.data_voltage_c
	# 		dds_dict['data_current_a'] = dds.data_current_a
	# 		dds_dict['data_current_b'] = dds.data_current_b
	# 		dds_dict['data_current_c'] = dds.data_current_c
	# 		dds_dict['data_total_va'] = dds.data_total_va
	#
	# 		dd_by_location_list.append(dds_dict)

	serailized_dd = serialize('json', meters, indent=2)
	# serailized_dc_locations = json.dumps(meters, default=datetime_handler)
	return HttpResponse(serailized_dd, content_type="application/json")


def redirect_to_dashboard(request):
    	return HttpResponseRedirect('/user/dashboard/')
