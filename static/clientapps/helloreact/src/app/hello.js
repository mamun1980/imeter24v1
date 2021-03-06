import React from 'react';
import { render } from 'react-dom';
import axios from 'axios';

let users = [
{
  "model": "Contacts.contacts",
  "pk": 5,
  "fields": {
    "customer_name": "Default Guest Login",
    "attention_to": "",
    "webpage": "",
    "address_1": "",
    "address_2": "",
    "city": "",
    "province": "Ontario",
    "country": "Canada",
    "postal_code": "",
    "gst_tax_exempt": false,
    "hst_tax_exempt": false,
    "pst_tax_exempt": false,
    "terms": 1,
    "gst_number": "",
    "hst_number": "",
    "contact_type": 1,
    "pst_number": "",
    "foreign_account": "",
    "delivery_type": 1,
    "ship_collect": false,
    "currency_type": 1,
    "fob": "Oshawa, Ontario, Canada",
    "ap_contact": "",
    "comments": "",
    "record_created": "2016-11-28",
    "last_activity": null
  }
},
{
  "model": "Contacts.contacts",
  "pk": 4,
  "fields": {
    "customer_name": "Intellimeter Canada",
    "attention_to": "",
    "webpage": "",
    "address_1": "",
    "address_2": "",
    "city": "",
    "province": "Ontario",
    "country": "Canada",
    "postal_code": "",
    "gst_tax_exempt": false,
    "hst_tax_exempt": false,
    "pst_tax_exempt": false,
    "terms": 1,
    "gst_number": "",
    "hst_number": "",
    "contact_type": 1,
    "pst_number": "",
    "foreign_account": "",
    "delivery_type": 1,
    "ship_collect": false,
    "currency_type": 1,
    "fob": "Oshawa, Ontario, Canada",
    "ap_contact": "",
    "comments": "",
    "record_created": "2016-11-28",
    "last_activity": null
  }
},
{
  "model": "Contacts.contacts",
  "pk": 6,
  "fields": {
    "customer_name": "Known ODROID Login",
    "attention_to": "",
    "webpage": "",
    "address_1": "",
    "address_2": "",
    "city": "",
    "province": "Ontario",
    "country": "Canada",
    "postal_code": "",
    "gst_tax_exempt": false,
    "hst_tax_exempt": false,
    "pst_tax_exempt": false,
    "terms": 1,
    "gst_number": "",
    "hst_number": "",
    "contact_type": 1,
    "pst_number": "",
    "foreign_account": "",
    "delivery_type": 1,
    "ship_collect": false,
    "currency_type": 1,
    "fob": "Oshawa, Ontario, Canada",
    "ap_contact": "",
    "comments": "",
    "record_created": "2016-12-05",
    "last_activity": null
  }
},
{
  "model": "Contacts.contacts",
  "pk": 1,
  "fields": {
    "customer_name": "Paul Kudla",
    "attention_to": "",
    "webpage": "",
    "address_1": "730 Breezy Drive",
    "address_2": "Unit 10",
    "city": "Pickering",
    "province": "Ontario",
    "country": "",
    "postal_code": "L1J7E8",
    "gst_tax_exempt": false,
    "hst_tax_exempt": false,
    "pst_tax_exempt": false,
    "terms": 3,
    "gst_number": "",
    "hst_number": "",
    "contact_type": 1,
    "pst_number": "",
    "foreign_account": "",
    "delivery_type": 1,
    "ship_collect": false,
    "currency_type": 1,
    "fob": "",
    "ap_contact": "",
    "comments": "",
    "record_created": null,
    "last_activity": null
  }
},
{
  "model": "Contacts.contacts",
  "pk": 3,
  "fields": {
    "customer_name": "Paul Kudla Jr",
    "attention_to": null,
    "webpage": "www.scom.ca",
    "address_1": null,
    "address_2": null,
    "city": null,
    "province": "Ontario",
    "country": "Canada",
    "postal_code": null,
    "gst_tax_exempt": false,
    "hst_tax_exempt": false,
    "pst_tax_exempt": false,
    "terms": 1,
    "gst_number": null,
    "hst_number": null,
    "contact_type": 1,
    "pst_number": null,
    "foreign_account": null,
    "delivery_type": 1,
    "ship_collect": false,
    "currency_type": 1,
    "fob": "Oshawa, Ontario, Canada",
    "ap_contact": null,
    "comments": null,
    "record_created": "2016-10-08",
    "last_activity": null
  }
},
{
  "model": "Contacts.contacts",
  "pk": 2,
  "fields": {
    "customer_name": "Tom Kudla Jr",
    "attention_to": "",
    "webpage": "",
    "address_1": "",
    "address_2": "",
    "city": "",
    "province": "",
    "country": "",
    "postal_code": "",
    "gst_tax_exempt": false,
    "hst_tax_exempt": false,
    "pst_tax_exempt": false,
    "terms": 1,
    "gst_number": "",
    "hst_number": "",
    "contact_type": 1,
    "pst_number": "",
    "foreign_account": "",
    "delivery_type": 1,
    "ship_collect": false,
    "currency_type": 1,
    "fob": "",
    "ap_contact": "",
    "comments": "",
    "record_created": "2016-08-28",
    "last_activity": null
  }
}
]