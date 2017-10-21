# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from imeter24.site import site

from .models import *
# Register your models here.

site.register(MeterRead)