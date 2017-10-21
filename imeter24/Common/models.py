#Common Text Model for test of system

#from django.db import models

# Create your models here.
#Premier Elevator Common Pull Down Text Application



phone_type_choices = (
	('main', 'main'),
	('home', 'home'),
	('work', 'work'),
	('mobile', 'mobile'),
	('pager', 'pager'),
	('other', 'other'),
	('fax', 'fax'),
)

payment_terms_choices = (
	('COD', 'Cash On Delivery'),
	('COD-CERT', 'COD with Certified Cheque'),
	('Advance', 'Pre-payment Required'),
	('NET', 'NET - Due Upon Reciept'),
	('NET-5', 'Payment due within 5 days'),
	('NET-7', 'Payment due within 7 days'),
	('NET-10', 'Payment due within 10 days'),
	('NET-15', 'Payment due within 15 days'),
	('NET-20', 'Payment due within 20 days'),
	('NET-30', 'Payment due within 30 days'),
)

record_type_choice = (
    ('customer', 'Customer'),
    ('supplier', 'Supplier'),
    ('both', 'Customer and Supplier'),
)


mail_list_type_choices = (
    ('YES', 'Yes'),
    ('NO', 'No'),
)

shipping_method_choices = (
    ('pickup', 'Pickup'),
    ('our_truck', 'Our Truck'),
    ('purolater', 'Purolator'),
    ('FedEx', 'Federal Express'),
    ('UPS', 'United Parcel Service'),
    ('mail', 'Canada Post'),
    ('other', 'Other'),
)
# Full list: http://www.xe.com/iso4217.php
# EU members: http://www.xe.com/euro.php
currency_choices = (
    ('CAD', 'Canadian'),
    ('USD', 'US'),
    ('GBP', 'British Pounds'),
    ('EUR', 'Euros'),
    ('CHF', "Swiss Franks")
)

portal_account_type_choices = (
	('EX', 'External Billing'),
	('PWK', 'Billed by Paul Kudla'),
	('REF', 'Referal Account (Free)'),
)

serverstatus_choices = (
	('Off', 'Offline'),
	('On', 'On Line - Waiting for Call'),
	('Bsy', 'On Line - In Session'),
)

serveraction_choices = (
	('NONE', 'None'),
	('EMAIL', 'Email Reported Issue'),
	('CALL', 'Call to Phone Number'),
	('BOTH', 'Both Call & Email'),
)

serveraction_status = (
	('NONE', 'None'),
	('UP', 'Online'),
	('DOWN','Down'),
	('ERROR', 'Hardware Error'),
)

runtype_choices = (
	('NONE','None (Select)'),
	('MATCH','Match Subject - OK'),
)	

