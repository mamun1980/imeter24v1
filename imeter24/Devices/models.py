from django.db import models

from imeter24.Config.models import Config_Data,Config_Contact_Type,Config_Payment_Terms,Config_Email_Type,Config_Delivery_Type,Distribution_Type
from imeter24.Config.models import Currency_Type,Phone_Type,Config_Hardware_Type

from imeter24.Contacts.models import Contacts

class Devices_Config(models.Model):
	id = models.AutoField(primary_key=True) 																#General Data Id
	datecreated = models.DateTimeField(verbose_name='Device Created', null=True, blank=True)				#Dae this Data/Device came into service
	soldto = models.ForeignKey(Contacts,default = None,null=True, blank=True,related_name = 'soldto_devices_config')												#Sold to (Bill to) Info
	siteid = models.ForeignKey(Contacts,default = None,null=True, blank=True,related_name = 'siteid_devices_config')					#Physical Address that device is located
	locationid = models.TextField(verbose_name = 'Location',max_length=100,default = None,null=True, blank=True,)				#Physical Location Inside Physical Adress Used to Id the Physical Meter
	modelid = 	models.ForeignKey(Config_Hardware_Type,default = None,null=True, blank=True,related_name = 'devices_config_modelid')					#Model ID of Device (aka i45, 636,mf12,display etc)
	lastdbread = models.DateTimeField(verbose_name='Last DB Read', null=True, blank=True)					#Date that last time we talked to this device
	device_disabled = models.BooleanField(verbose_name='Disabled', null=False, default=False)
	comments = models.TextField(verbose_name = 'Comments',max_length=100,default = None,null=True, blank=True,)

	device_filename = models.CharField(verbose_name='Access File', max_length=40, null=True, blank=True)		#Used to access the remote saved data (updates)
	device_login = models.CharField(verbose_name='Login Id or MAC Address', max_length=32, null=True, blank=True)
	device_port = models.CharField(verbose_name='Device Port', max_length=40, null=True, blank=True)			#The port on this meter being accessed (aka /dev/ttyUSB0)
	device_address = models.IntegerField(verbose_name='ModBus',null=True, blank=True)					#Meter Address (Actual Modbus Address)
	device_register = models.IntegerField(verbose_name='Register',null=True, blank=True)	#Actual Meter register being read 1100,1200 etc
	device_serial_number = models.BigIntegerField(verbose_name='Device Serial Number',null=True, blank=True) #Unit Serial Number (Used to ID Device)
	device_firmware = models.IntegerField(verbose_name='Firmware Revision',null=True, blank=True)			#Firware version (for reference)
	device_oem = models.CharField(verbose_name='OEM', max_length=3, null=True, blank=True)					#
	device_model = models.IntegerField(verbose_name='Device ID From Meter',null=True, blank=True)					#Model Number

	device_v_multiplier = models.IntegerField(verbose_name='V Multiplier',null=True, blank=True)
	device_v_divider = models.IntegerField(verbose_name='V Divider',null=True, blank=True)
	device_i_multiplier = models.IntegerField(verbose_name='I Multiplier',null=True, blank=True)
	device_i_divider = models.IntegerField(verbose_name='I Divider',null=True, blank=True)
	device_p_multiplier = models.IntegerField(verbose_name='P Multiplier',null=True, blank=True)
	device_p_divider = models.IntegerField(verbose_name='P Divider',null=True, blank=True)
	device_agl_multiplier = models.IntegerField(verbose_name='AGL Multiplier',null=True, blank=True)
	device_agl_divider = models.IntegerField(verbose_name='AGL Divider',null=True, blank=True)

	device_elements = models.IntegerField(verbose_name='Elements',null=True, blank=True)						#Elements
	device_numberofmeters = models.IntegerField(verbose_name='Number of Meters',null=True, blank=True)				#Number of Meters Avaliable for read.


	class Meta:
		ordering = ['soldto', 'siteid']
		db_table = u'device_config'
		verbose_name = u"Device Config"
		verbose_name_plural = u"Device Config"

	def __unicode__(self):
		return unicode(self.datecreated)



class Devices_Data(models.Model):																				#This is the data being held for the device (formatted to support ALL Devices)
	id = models.AutoField(primary_key=True)
	datecreated = models.DateTimeField(verbose_name='Read Created', null=True, blank=True)
	soldto = models.ForeignKey(Contacts,default = None,null=True, blank=True,related_name = 'soldto_devices_data')												#Sold to (Bill to) Info
	siteid = models.ForeignKey(Contacts,default = None,null=True, blank=True,related_name = 'siteid_devices_data')					#Physical Address that device is located
	locationid = models.TextField(verbose_name = 'Location',max_length=100,default = None,null=True, blank=True,)	#Physical Location Inside Physical Adress Used to Id the Physical Meter
	comments = models.TextField(verbose_name = 'Comments',max_length=100,default = None,null=True, blank=True,)
	login = models.CharField(verbose_name='Login Id or MAC Address', max_length=32, null=True, blank=True)
	modelid = 	models.ForeignKey(Config_Hardware_Type,default = None,null=True, blank=True,related_name = 'devices_data_modelid')						#Model ID of Device (aka i45, 636,mf12,display etc)
	device_address = models.IntegerField(verbose_name='ModBus',null=True, blank=True)					#Meter Address (Actual Modbus Address)
	device_register = models.IntegerField(verbose_name='Register',null=True, blank=True)	#Actual Meter register being read 1100,1200 etc
	device_serial_number = models.BigIntegerField(verbose_name='Device Serial Number',null=True, blank=True) #Unit Serial Number (Used to ID Device)
	device_read_status = models.CharField(verbose_name='Read Status', max_length=20, null=True, blank=True)
	data_timestamp = models.DateTimeField(verbose_name='Actual Read', null=True, blank=True)									#Data Timestamp

	data_active_phase = models.IntegerField(verbose_name='Active Phase', null=True, blank=True)
	data_voltage_a = models.DecimalField(verbose_name='Voltage A', max_digits=12, decimal_places=2, null=True, blank=True)
	data_voltage_b = models.DecimalField(verbose_name='Voltage B', max_digits=12, decimal_places=2, null=True, blank=True)
	data_voltage_c = models.DecimalField(verbose_name='Voltage C', max_digits=12, decimal_places=2, null=True, blank=True)
	data_current_a = models.DecimalField(verbose_name='Current A', max_digits=12, decimal_places=2, null=True, blank=True)
	data_current_b = models.DecimalField(verbose_name='Current B', max_digits=12, decimal_places=2, null=True, blank=True)
	data_current_c = models.DecimalField(verbose_name='Current C', max_digits=12, decimal_places=2, null=True, blank=True)
	data_watts_a = models.DecimalField(verbose_name='Wattage A', max_digits=12, decimal_places=2, null=True, blank=True)
	data_watts_b = models.DecimalField(verbose_name='Wattage B', max_digits=12, decimal_places=2, null=True, blank=True)
	data_watts_c = models.DecimalField(verbose_name='Wattage C', max_digits=12, decimal_places=2, null=True, blank=True)
	data_va_a = models.DecimalField(verbose_name='VA Reading A', max_digits=12, decimal_places=2, null=True, blank=True)
	data_va_b = models.DecimalField(verbose_name='VA Reading B', max_digits=12, decimal_places=2, null=True, blank=True)
	data_va_c = models.DecimalField(verbose_name='VA Reading C', max_digits=12, decimal_places=2, null=True, blank=True)
	data_var_a = models.DecimalField(verbose_name='VAR Reading A', max_digits=12, decimal_places=2, null=True, blank=True)
	data_var_b = models.DecimalField(verbose_name='VAR Reading B', max_digits=12, decimal_places=2, null=True, blank=True)
	data_var_c = models.DecimalField(verbose_name='VAR REading C', max_digits=12, decimal_places=2, null=True, blank=True)
	data_power_factor_a = models.DecimalField(verbose_name='Power Factor A', max_digits=12, decimal_places=2, null=True, blank=True)
	data_power_factor_b = models.DecimalField(verbose_name='Power Factor B', max_digits=12, decimal_places=2, null=True, blank=True)
	data_power_factor_c = models.DecimalField(verbose_name='Power Factor C', max_digits=12, decimal_places=2, null=True, blank=True)
	data_kwatts = models.DecimalField(verbose_name='Total kWh', max_digits=12, decimal_places=2, null=True, blank=True)
	data_kva = models.DecimalField(verbose_name='Total kVAh', max_digits=12, decimal_places=2, null=True, blank=True)
	data_frequency = models.DecimalField(verbose_name='Frequency', max_digits=12, decimal_places=2, null=True, blank=True)
	data_voltage_average = models.DecimalField(verbose_name='kVARh Avg', max_digits=12, decimal_places=2, null=True, blank=True)
	data_total_current = models.DecimalField(verbose_name='Total Current (This Read)', max_digits=12, decimal_places=2, null=True, blank=True)
	data_total_watts = models.DecimalField(verbose_name='Total Wattage (This Read)', max_digits=12, decimal_places=2, null=True, blank=True)
	data_total_va = models.DecimalField(verbose_name='Total VA (This Read)', max_digits=12, decimal_places=2, null=True, blank=True)
	remote_id = models.IntegerField(verbose_name='Remote Record ID',null=True, blank=True)

	class Meta:
		ordering = ['soldto','siteid']
		db_table = u'device_data'
		verbose_name = u"Meter Device Read Data"
		verbose_name_plural = u"Meter Device Read Data"

	#def __unicode__(self):
	#	return self.datecreated


class Devices_Relays(models.Model):																				#This is the data being held for the device (formatted to support ALL Devices)
	id = models.AutoField(primary_key=True)
	datecreated = models.DateTimeField(verbose_name='Read Created', null=True, blank=True)
	soldto = models.ForeignKey(Contacts,default = None,null=True, blank=True,related_name = 'soldto_devices_relays')												#Sold to (Bill to) Info
	siteid = models.ForeignKey(Contacts,default = None,null=True, blank=True,related_name = 'siteid_devices_relays')					#Physical Address that device is located
	locationid = models.TextField(verbose_name = 'Location',max_length=100,default = None,null=True, blank=True,)					#Physical Location Inside Physical Adress Used to Id the Physical Meter
	modelid = 	models.ForeignKey(Config_Hardware_Type,default = None,null=True, blank=True,related_name = 'devices_relays_modelid')						#Model ID of Device (aka i45, 636,mf12,display etc)
	device_address = models.IntegerField(verbose_name='ModBus',null=True, blank=True)					#Meter Address (Actual Modbus Address)
	device_register = models.IntegerField(verbose_name='Register',null=True, blank=True)	#Actual Meter register being read 1100,1200 etc
	device_serial_number = models.BigIntegerField(verbose_name='Device Serial Number',null=True, blank=True) #Unit Serial Number (Used to ID Device)
	device_read_status = models.CharField(verbose_name='Read Status', max_length=20, null=True, blank=True)
	data_timestamp = models.DateTimeField(verbose_name='Actual Read', null=True, blank=True)

	class Meta:
		ordering = ['soldto', 'siteid']
		db_table = u'device_relays'
		verbose_name = u"Relay Status Data"
		verbose_name_plural = u"Relay Status Data"

class Devices_Relay_Contact_Status(models.Model):
	relay_form		= models.ForeignKey(Devices_Relays,related_name='device_relays_unit', unique=False)
	relay_number	= models.IntegerField(verbose_name='Relay', null=False, blank=False)
	relay_description = models.CharField(verbose_name='Description', max_length=32, null=True, blank=True)
	relay_state		= models.BooleanField(verbose_name='State', null=False, default=False)



class Devices_Displays(models.Model):																				#This is the data being held for the device (formatted to support ALL Devices)
	id = models.AutoField(primary_key=True)
	datecreated = models.DateTimeField(verbose_name='Read Created', null=True, blank=True)
	soldto = models.ForeignKey(Contacts,default = None,null=True, blank=True,related_name = 'soldto_devices_displays')												#Sold to (Bill to) Info
	siteid = models.ForeignKey(Contacts,default = None,null=True, blank=True,related_name = 'siteid_devices_displays')					#Physical Address that device is located
	locationid = models.TextField(verbose_name = 'Location',max_length=100,default = None,null=True, blank=True,)					#Physical Location Inside Physical Adress Used to Id the Physical Meter
	modelid = 	models.ForeignKey(Config_Hardware_Type,default = None,null=True, blank=True,related_name = 'devices_displays_modelid')						#Model ID of Device (aka i45, 636,mf12,display etc)
	device_address = models.IntegerField(verbose_name='ModBus',null=True, blank=True)					#Meter Address (Actual Modbus Address)
	device_register = models.IntegerField(verbose_name='Register',null=True, blank=True)	#Actual Meter register being read 1100,1200 etc
	device_serial_number = models.BigIntegerField(verbose_name='Device Serial Number',null=True, blank=True) #Unit Serial Number (Used to ID Device)
	device_read_status = models.CharField(verbose_name='Read Status', max_length=20, null=True, blank=True)
	data_timestamp = models.DateTimeField(verbose_name='Actual Read', null=True, blank=True)
	message_sent = models.CharField(verbose_name='Message Sent', max_length=100, null=True, blank=True)

	class Meta:
		ordering = ['soldto', 'siteid']
		db_table = u'device_displays'
		verbose_name = u"Display History Data"
		verbose_name_plural = u"Display History Data"
