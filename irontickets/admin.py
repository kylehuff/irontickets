from models import *
from django.contrib import admin
from attachments.admin import AttachmentInlines

class TicketPriorityAdmin(admin.ModelAdmin):
    list_display = ('priority', 'name', 'showinportal')
    ordering = ('priority', 'name')

class TicketAdmin(admin.ModelAdmin):
    inlines = [AttachmentInlines]

admin.site.register(TicketPriority, TicketPriorityAdmin)

admin.site.register(CompanyType)
admin.site.register(CompanyStatus)
admin.site.register(Company)
admin.site.register(TechStream)
admin.site.register(TicketStatus)
admin.site.register(TicketSource)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(ContactTitle)
admin.site.register(AddressType)
admin.site.register(Address)
admin.site.register(PhoneLocation)
admin.site.register(Phone)
admin.site.register(ITProfile)
admin.site.register(Theme)
