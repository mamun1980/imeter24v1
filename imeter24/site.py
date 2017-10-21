from django.contrib.auth.admin import Group, GroupAdmin, User, UserAdmin

from imeter24.adminextra.site import AdminSiteWithOps


site = AdminSiteWithOps()
site.register(Group, GroupAdmin)
site.register(User, UserAdmin)
