# Admin module
from imeter24.site import site

from imeter24.Devices.models import Devices_Config,Devices_Data,Devices_Relays,Devices_Displays,Devices_Relay_Contact_Status
from django.contrib import admin


class Devices_Config_Admin(admin.ModelAdmin):
	'''We want to customize our admin display'''
	fieldsets = [
		('Device Identifier',    {'fields': ['datecreated', 'device_address','device_register','device_serial_number','device_disabled']}),
		('Contact Data',    {'fields': ['soldto','siteid','locationid','comments','modelid','lastdbread', ]}),
		('Device Info',    {'fields': ['device_login','device_filename','device_port','device_address','device_register','device_serial_number','device_firmware','device_oem','device_model' ]}),
		('Device Data',    {'fields': ['device_v_multiplier','device_v_divider', 'device_i_multiplier','device_i_divider','device_p_multiplier','device_p_divider', 'device_agl_multiplier','device_agl_divider',]}),
		('Device ',    {'fields': ['device_elements','device_numberofmeters', ]}),
	]
	ordering = ('-lastdbread',)
	index = False
	#list_display = ('id', 'locationid','device_address','device_filename','device_serial_number','device_model','device_register',)
	list_display = ('id','soldto','locationid','comments','modelid','device_disabled','lastdbread','device_address','device_register','device_elements','device_numberofmeters')
	#search_fields = ['locationid', 'device_address','device_filename','device_serial_number','device_model', ]
	search_fields = ['locationid','comments']



site.register(Devices_Config, Devices_Config_Admin)


class Devices_Data_Admin(admin.ModelAdmin):
	'''We want to customize our admin display'''
	fieldsets = [
		#('Device Identifier',    {'fields': ['id', ]}),
		('Contact Data',    {'fields': ['soldto','siteid','login','locationid','comments','modelid','data_timestamp','device_read_status','datecreated','device_address','device_register','device_serial_number', ]}),
		('Cumilative Read Data',    {'fields': [('data_kwatts','data_kva','data_voltage_average',) ]}),
		('This Read Data',    {'fields': [('data_total_va','data_total_current','data_total_watts','data_frequency',) ]}),
		('VAR Readings',    {'fields': [('data_var_a','data_var_b','data_var_c',) ]}),
		('VA Readings',    {'fields': [('data_va_a','data_va_b','data_va_c',) ]}),
		('Watt Readings',    {'fields': [('data_watts_a','data_watts_b','data_watts_c',) ]}),
		('Current Readings',    {'fields': [('data_current_a', 'data_current_b','data_current_c',) ]}),
		('Voltage Readings',    {'fields': [( 'data_voltage_a', 'data_voltage_b', 'data_voltage_c','data_active_phase',) ]}),
		('Power Factor',    {'fields': [('data_power_factor_a','data_power_factor_b','data_power_factor_c',) ]}),
	]
	index = False
	list_display = ('id','locationid','comments','data_timestamp','datecreated','device_read_status','data_kwatts','data_kva','data_voltage_average','device_address','device_register',)
	#search_fields = ['id','soldto','siteid','locationid','modelid','device_address','device_register','device_serial_number']
	search_fields = ['locationid','comments']
	ordering = ('-data_timestamp',)



site.register(Devices_Data, Devices_Data_Admin)

class Devices_Relay_Contact_Status_Inline(admin.TabularInline):
	model = Devices_Relay_Contact_Status
	extra = 1



class Devices_Relays_Admin(admin.ModelAdmin):
	'''We want to customize our admin display'''
	inlines = [Devices_Relay_Contact_Status_Inline, ]
	fieldsets = [
		#('Device Identifier',    {'fields': ['id', ]}),
		('Contact Data',    {'fields': ['soldto','siteid','locationid','modelid','data_timestamp','device_read_status','datecreated', ]}),

	]
	index = False
	list_display = ('locationid','device_address','device_register','data_timestamp','datecreated','device_read_status',)
	#search_fields = ['id','soldto','siteid','locationid','modelid','device_address','device_register','device_serial_number']
	search_fields = ['device_address','device_register','device_serial_number',]



site.register(Devices_Relays, Devices_Relays_Admin)


class Devices_Displays_Admin(admin.ModelAdmin):
	'''We want to customize our admin display'''
	fieldsets = [
		#('Device Identifier',    {'fields': ['id', ]}),
		('Contact Data',    {'fields': ['soldto','siteid','locationid','modelid','data_timestamp','device_read_status','datecreated','message_sent' ]}),

	]
	index = False
	list_display = ('locationid','device_address','device_register','data_timestamp','datecreated','device_read_status',)
	#search_fields = ['id','soldto','siteid','locationid','modelid','device_address','device_register','device_serial_number']
	search_fields = ['device_address','device_register','device_serial_number',]




site.register(Devices_Displays, Devices_Displays_Admin)
