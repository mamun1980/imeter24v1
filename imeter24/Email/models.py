from django.db import models
from django.core.signals import request_finished
#from django.core.signals import post_save
from django.dispatch import receiver
from lib import * #Get scom lib.py functions



action_choices = (
#    ('', 'None'),
    ('A', 'Add account to cyrus'),
    ('D', 'Delete account from cyrus'),
)

ip_action_choices = (
	('A', 'Allow'),
	('D', 'Deny'),
)

ip_program_choices = (
	('ALL', 'All'),
	('SSHD', 'SSH Access'),
	('MAIL','Mail Server'),
)


class Users(models.Model):
	username     = models.EmailField(max_length=64, primary_key=True, unique=True)
	password     = models.CharField(max_length=64)
	domain       = models.CharField(max_length=64)
	status       = models.BooleanField('Account Enabled?')
	destination  = models.EmailField(max_length=64)
	source       = models.EmailField(max_length=64)
	accountid    = models.CharField(max_length=10,verbose_name='Account Number')
	mailscanner  = models.BooleanField('Mail Scanner?')
	virusscanner = models.BooleanField('Virus Scanner?')
	poweruser    = models.BooleanField('Power User?')
	action       = models.CharField(max_length=1, choices=action_choices, verbose_name='User action pending', null=True, blank=True)
	accountsize	 = models.CharField(max_length=20,verbose_name='Mailbox Size', blank=True,null=True)
	last_updated = models.DateField(verbose_name='Mail Box Last Updated', blank=True,null=True)
	last_accessed = models.DateField(verbose_name='Mail Box Last Accessed', blank=True,null=True)
	last_updated_time = models.TimeField(verbose_name='Mail Box Last Updated', blank=True,null=True)
	last_accessed_time = models.TimeField(verbose_name='Mail Box Last Updated', blank=True,null=True)
	messagecount = models.CharField(verbose_name='Message Count', max_length=15, null=True, blank=True)
	daystoholdemails = models.IntegerField(verbose_name='Days Till Deletion', null=True, blank=True, default='0')
	currentcount = models.IntegerField(verbose_name='Current Hourly Count', null=True, blank=True, default='0')
	maxcount	   = models.IntegerField(verbose_name='Max Threshold', null=True, blank=True, default='0')



	class Meta:
		ordering = ['username',]
		db_table = u'email_users'
		verbose_name = u"User"
		verbose_name_plural = u"User List"

	@receiver(request_finished)
	def my_callback(sender, **kwargs):
		arguments = kwargs
		send_from = 'power@scom.ca'
		send_files = []
		send_to = ['power@scom.ca',]
		send_subject = 'test message form django email screen'
		send_text = repr(sender) + '\n' + repr(dir(sender)) +'\n\n' + repr(arguments) + '\n' + repr((arguments['signal'].receivers))
		#sendmail(send_from,send_to,send_subject,send_text,send_files,'mail.scom.ca','paul@scom.ca','sc366399') #Send the warning email




	def __unicode__(self):
		return self.username



class IpBlock(models.Model):
	id 			= models.AutoField(primary_key=True)
	program 	= models.CharField(max_length=15, choices=ip_program_choices, verbose_name='Program', default = 'ALL', null=True, blank=True)
	ipaddress 	= models.CharField(verbose_name='IP Address', max_length=40, null=True, blank=False)
	action      = models.CharField(max_length=15, choices=ip_action_choices, verbose_name='Action', default = 'D', null=True, blank=True)
	comments	= models.TextField(verbose_name='Comments', max_length=200, null=True, blank=True, default = 'Denied due to Unauthorized Use')

	class Meta:
		ordering = ['program',]
		db_table = u'blocked_ip'
		verbose_name = u"Blocked IP's"
		verbose_name_plural = u"Blocked Ip's"

	def __unicode__(self):
		return self.program


class BlackListServers(models.Model):
	server		= models.CharField(verbose_name='Server', max_length=64, primary_key=True, unique=True)
	servername	= models.CharField(verbose_name='Name', max_length=128, null=True, blank=True, default = '')
	serverlink  = models.CharField(verbose_name='Link', max_length=200, null=True, blank=True, default = '')
	active		= models.BooleanField('Active')
	comments	= models.TextField(verbose_name='Comments', max_length=200, null=True, blank=True, default = '')

	class Meta:
		ordering = ['server',]
		db_table = u'black_list_servers'
		verbose_name = u"Black List Server"
		verbose_name_plural = u"Black List Server's"

	def __unicode__(self):
		return self.server

class IpCount(models.Model):
	ipaddress 	= models.GenericIPAddressField(verbose_name='IP Address', max_length=17,blank=False,primary_key=True, unique=True)
	counthour   = models.IntegerField(verbose_name='Current IP Count This Hour', null=True, blank=True, default='0')
	counttotal  = models.IntegerField(verbose_name='Total IP Count to Date', null=True, blank=True, default='0')
	comments	= models.TextField(verbose_name='Comments', max_length=500, null=True, blank=True, default = '')

	class Meta:
		ordering = ['ipaddress',]
		db_table = u'ip_count'
		verbose_name = u"IP Count"
		verbose_name_plural = u"IP Counts"

	def __unicode__(self):
		return self.ipaddress


class TMDA_Whitelist(models.Model):
	id 			= models.AutoField(primary_key=True)
	username 	= models.CharField(verbose_name='SCOM Username', max_length=64, null=True, blank=False)
	address 	= models.CharField(verbose_name='TMDA Match Address', max_length=64, null=True, blank=False)

	class Meta:
		ordering = ['username','address',]
		db_table = u'tmda_whitelist'
		verbose_name = u"TMDA Whitelist"
		verbose_name_plural = u"TMDA Whitelist"

	def __unicode__(self):
		return self.username


class TMDA_Blacklist(models.Model):
	id 			= models.AutoField(primary_key=True)
	username 	= models.CharField(verbose_name='SCOM Username', max_length=64, null=True, blank=False)
	address 	= models.CharField(verbose_name='TMDA Match Address', max_length=64, null=True, blank=False)

	class Meta:
		ordering = ['username','address',]
		db_table = u'tmda_blacklist'
		verbose_name = u"TMDA Blacklist"
		verbose_name_plural = u"TMDA Blacklist"

	def __unicode__(self):
		return self.username
