from django.db import models

class Config_Data(models.Model):
	variable = models.CharField(verbose_name='Variable', max_length=32, null=False, blank=False,primary_key=True)
	value = models.CharField(verbose_name='Value', max_length = 64,null=True)
	comments = models.CharField(verbose_name='Comments', max_length = 32,null=True)
	
	class Meta:
		ordering = ['variable', 'value']
		db_table = u'system_config_data'
		verbose_name = u"System Config Data"
		verbose_name_plural = u"System Config Data"

	def __unicode__(self):
		return self.variable


class Config_Contact_Type(models.Model):
	id = models.AutoField(verbose_name='Id', null=False, blank=False, editable=False, primary_key=True)
	type = models.CharField(verbose_name='Type', max_length=40, null=False, blank=False, )
	comments = models.CharField(verbose_name='Comments', max_length=40, null=True, blank=True)
	
	class Meta:
		ordering = ['id',]
		db_table = u'config_contact_type'
		verbose_name = u"Contact Mail List Type"
		verbose_name_plural = u"Contact Mail List Type"

	def __unicode__(self):
		return self.type
		
class Config_Payment_Terms(models.Model):
	id = models.AutoField(verbose_name='Id', null=False, blank=False, editable=False, primary_key=True)
	type = models.CharField(verbose_name='Term(s)', max_length=40, null=False, blank=False, )
	comments = models.CharField(verbose_name='Comments', max_length=40, null=True, blank=True)
	
	class Meta:
		ordering = ['id',]
		db_table = u'config_payment_terms'
		verbose_name = u"Terms"
		verbose_name_plural = u"Terms"

	def __unicode__(self):
		return self.type
		
class Config_Email_Type(models.Model):
	id = models.AutoField(verbose_name='Id', null=False, blank=False, editable=False, primary_key=True)
	type = models.CharField(verbose_name='Email Type', max_length=40, null=False, blank=False, )
	comments = models.CharField(verbose_name='Comments', max_length=40, null=True, blank=True)
	
	class Meta:
		ordering = ['id',]
		db_table = u'config_email_type'
		verbose_name = u"Email Type"
		verbose_name_plural = u"Email Type"

	def __unicode__(self):
		return self.type
		
		
class Config_Delivery_Type(models.Model):
	id = models.AutoField(verbose_name='Id', null=False, blank=False, editable=False, primary_key=True)
	type = models.CharField(verbose_name='Delivery Type', max_length=40, null=False, blank=False, )
	comments = models.CharField(verbose_name='Comments', max_length=40, null=True, blank=True)
	
	class Meta:
		ordering = ['id',]
		db_table = u'config_delivery_type'
		verbose_name = u"Delivery Type"
		verbose_name_plural = u"Delivery Type"

	def __unicode__(self):
		return self.type
		
class Distribution_Type(models.Model):
	id = models.AutoField(verbose_name='Id', null=False, blank=False, editable=False, primary_key=True)
	type = models.CharField(verbose_name='Distribution Type', max_length=40, null=False, blank=False, )
	comments = models.CharField(verbose_name='Comments', max_length=40, null=True, blank=True)
	
	class Meta:
		ordering = ['id',]
		db_table = u'config_distribution_type'
		verbose_name = u"Distribution Type"
		verbose_name_plural = u"Distribution Type"

	def __unicode__(self):
		return self.type
		
class Currency_Type(models.Model):
	id = models.AutoField(verbose_name='Id', null=False, blank=False, editable=False, primary_key=True)
	type = models.CharField(verbose_name='Currency Type', max_length=40, null=False, blank=False, )
	comments = models.CharField(verbose_name='Comments', max_length=40, null=True, blank=True)
	
	class Meta:
		ordering = ['id',]
		db_table = u'config_currency_type'
		verbose_name = u"Currency Type"
		verbose_name_plural = u"Currency Type"

	def __unicode__(self):
		return self.type
		
class Phone_Type(models.Model):
	id = models.AutoField(verbose_name='Id', null=False, blank=False, editable=False, primary_key=True)
	type = models.CharField(verbose_name='Phone Type', max_length=40, null=False, blank=False, )
	comments = models.CharField(verbose_name='Comments', max_length=40, null=True, blank=True)
	
	class Meta:
		ordering = ['id',]
		db_table = u'config_phone_type'
		verbose_name = u"Phone Type"
		verbose_name_plural = u"Phone Type"

	def __unicode__(self):
		return self.type
		
class Config_Hardware_Type(models.Model):
	id = models.AutoField(verbose_name='Id', null=False, blank=False, editable=False, primary_key=True)
	type = models.CharField(verbose_name='Hardware Model', max_length=40, null=False, blank=False, )
	comments = models.CharField(verbose_name='Comments', max_length=40, null=True, blank=True)
	
	class Meta:
		ordering = ['id',]
		db_table = u'config_hardware_type'
		verbose_name = u"Hardware Type"
		verbose_name_plural = u"Hardware Type"

	def __unicode__(self):
		return self.type