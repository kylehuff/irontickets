from models import *
from django.contrib import admin

class TicketPriorityAdmin(admin.ModelAdmin):
    list_display = ('priority', 'name', 'showinportal')
    ordering = ('priority', 'name')

admin.site.register(TicketPriority, TicketPriorityAdmin)

admin.site.register(CompanyType)
admin.site.register(CompanyStatus)
admin.site.register(Company)
admin.site.register(TicketStatus)
admin.site.register(TicketSource)
admin.site.register(Ticket)
admin.site.register(ContactTitle)
admin.site.register(AddressType)
admin.site.register(Address)
admin.site.register(PhoneLocation)
admin.site.register(Phone)
admin.site.register(ITProfile)
admin.site.register(Theme)
