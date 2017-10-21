from django.db import models

class DNS_Data(models.Model):
    id = models.AutoField(primary_key=True)
    zone = models.CharField(verbose_name='Zone', max_length=64, null=True, blank=False)
    ttl = models.IntegerField(verbose_name='TTL', default=3600, null=False)
    type = models.CharField(verbose_name='Record Type A,PTR,CNAME', max_length=10, null=True, blank=False)
    host = models.CharField(verbose_name='Host A=Name,PTR=IP', max_length=64, null=True, blank=False)
    data = models.CharField(verbose_name='Data A=IP, PTR=Name', max_length=255, null=True, blank=False)
    mx_priority = models.IntegerField(null=True, blank=True)
    primary_ns = models.CharField(max_length=64, default="", null=True, blank=True)
    resp_person = models.CharField(max_length=20, default="", null=True, blank=True)
    serial = models.IntegerField(blank=True, null=True)
    refresh = models.IntegerField(blank=True, null=True)
    retry = models.IntegerField(blank=True, null=True)
    expire = models.IntegerField(blank=True, null=True)
    minimum = models.IntegerField(blank=True, null=True)
    status = models.BooleanField(verbose_name='Account Enabled?', blank=False, default=True)
    accountid = models.CharField(max_length=10,verbose_name='Account Number', null=True, blank=False)
    
    class Meta:
        ordering = ['zone', 'type']
        db_table = u'dns_data'
        verbose_name = u"DNS Data"
        verbose_name_plural = u"DNS/zone List"

    def __unicode__(self):
        return self.zone


class zonesorted(DNS_Data):
    class Meta:
        #ordering = ['zone', 'id']
        ordering = ['data', 'zone']
        proxy = True
