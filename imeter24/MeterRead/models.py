from django.db import models


class MeterRead(models.Model):
	meterread = models.CharField(max_length=64)


	class Meta:
		ordering = ['meterread']
		db_table = u'meterreads_dummy'
		verbose_name = u"Meter Reads"
		verbose_name_plural = u"Meter Reads"

	def __unicode__(self):
		return self.meterread
