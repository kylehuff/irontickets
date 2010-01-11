#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated, changes may be lost if you
# go and generate it again. It was generated with the following command:
# ./manage.py dumpscript irontickets

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

irontickets_companytype_1 = CompanyType()
irontickets_companytype_1.name = u'Client'
irontickets_companytype_1.save()
irontickets_companytype_2 = CompanyType()
irontickets_companytype_2.name = u'Competitor'
irontickets_companytype_2.save()
irontickets_companytype_3 = CompanyType()
irontickets_companytype_3.name = u'Supplier'
irontickets_companytype_3.save()
irontickets_companystatus_1 = CompanyStatus()
irontickets_companystatus_1.name = u'Collections'
irontickets_companystatus_1.active = False
irontickets_companystatus_1.save()
irontickets_companystatus_2 = CompanyStatus()
irontickets_companystatus_2.name = u'Inactive'
irontickets_companystatus_2.active = False
irontickets_companystatus_2.save()
irontickets_companystatus_3 = CompanyStatus()
irontickets_companystatus_3.name = u'Active'
irontickets_companystatus_3.active = True
irontickets_companystatus_3.save()
irontickets_contacttitle_1 = ContactTitle()
irontickets_contacttitle_1.title = u'Dr.'
irontickets_contacttitle_1.save()
irontickets_contacttitle_2 = ContactTitle()
irontickets_contacttitle_2.title = u'Miss'
irontickets_contacttitle_2.save()
irontickets_contacttitle_3 = ContactTitle()
irontickets_contacttitle_3.title = u'Mr.'
irontickets_contacttitle_3.save()
irontickets_contacttitle_4 = ContactTitle()
irontickets_contacttitle_4.title = u'Mrs.'
irontickets_contacttitle_4.save()
irontickets_contacttitle_5 = ContactTitle()
irontickets_contacttitle_5.title = u'Ms.'
irontickets_contacttitle_5.save()
irontickets_contacttitle_6 = ContactTitle()
irontickets_contacttitle_6.title = u'Prof.'
irontickets_contacttitle_6.save()
irontickets_contacttitle_7 = ContactTitle()
irontickets_contacttitle_7.title = u'Rev.'
irontickets_contacttitle_7.save()
irontickets_ticketstatus_1 = TicketStatus()
irontickets_ticketstatus_1.name = u'Closed'
irontickets_ticketstatus_1.isclosed = True
irontickets_ticketstatus_1.save()
irontickets_ticketstatus_2 = TicketStatus()
irontickets_ticketstatus_2.name = u'Completed'
irontickets_ticketstatus_2.isclosed = False
irontickets_ticketstatus_2.save()
irontickets_ticketstatus_3 = TicketStatus()
irontickets_ticketstatus_3.name = u'In Progress'
irontickets_ticketstatus_3.isclosed = False
irontickets_ticketstatus_3.save()
irontickets_ticketstatus_4 = TicketStatus()
irontickets_ticketstatus_4.name = u'New'
irontickets_ticketstatus_4.isclosed = False
irontickets_ticketstatus_4.save()
irontickets_ticketsource_1 = TicketSource()
irontickets_ticketsource_1.name = u'E-Mail'
irontickets_ticketsource_1.save()
irontickets_ticketsource_2 = TicketSource()
irontickets_ticketsource_2.name = u'IM'
irontickets_ticketsource_2.save()
irontickets_ticketsource_3 = TicketSource()
irontickets_ticketsource_3.name = u'On-Site'
irontickets_ticketsource_3.save()
irontickets_ticketsource_4 = TicketSource()
irontickets_ticketsource_4.name = u'Phone Call'
irontickets_ticketsource_4.save()
irontickets_ticketsource_5 = TicketSource()
irontickets_ticketsource_5.name = u'Portal'
irontickets_ticketsource_5.save()
irontickets_ticketsource_6 = TicketSource()
irontickets_ticketsource_6.name = u'Scheduler'
irontickets_ticketsource_6.save()
irontickets_ticketsource_7 = TicketSource()
irontickets_ticketsource_7.name = u'Website'
irontickets_ticketsource_7.save()
irontickets_ticketpriority_1 = TicketPriority()
irontickets_ticketpriority_1.name = u'Emergency'
irontickets_ticketpriority_1.priority = 0L
irontickets_ticketpriority_1.showinportal = True
irontickets_ticketpriority_1.save()
irontickets_ticketpriority_2 = TicketPriority()
irontickets_ticketpriority_2.name = u'Maintenance'
irontickets_ticketpriority_2.priority = 5L
irontickets_ticketpriority_2.showinportal = True
irontickets_ticketpriority_2.save()
irontickets_ticketpriority_3 = TicketPriority()
irontickets_ticketpriority_3.name = u'Normal'
irontickets_ticketpriority_3.priority = 3L
irontickets_ticketpriority_3.showinportal = True
irontickets_ticketpriority_3.save()
irontickets_ticketpriority_4 = TicketPriority()
irontickets_ticketpriority_4.name = u'Urgent'
irontickets_ticketpriority_4.priority = 1L
irontickets_ticketpriority_4.showinportal = True
irontickets_ticketpriority_4.save()
irontickets_addresstype_1 = AddressType()
irontickets_addresstype_1.name = u'Billing'
irontickets_addresstype_1.save()
irontickets_addresstype_2 = AddressType()
irontickets_addresstype_2.name = u'Home'
irontickets_addresstype_2.save()
irontickets_addresstype_3 = AddressType()
irontickets_addresstype_3.name = u'Mailing'
irontickets_addresstype_3.save()
irontickets_addresstype_4 = AddressType()
irontickets_addresstype_4.name = u'Shipping'
irontickets_addresstype_4.save()
irontickets_addresstype_5 = AddressType()
irontickets_addresstype_5.name = u'Work'
irontickets_addresstype_5.save()
irontickets_phonelocation_1 = PhoneLocation()
irontickets_phonelocation_1.Location = u'Cell'
irontickets_phonelocation_1.save()
irontickets_phonelocation_2 = PhoneLocation()
irontickets_phonelocation_2.Location = u'Home'
irontickets_phonelocation_2.save()
irontickets_phonelocation_3 = PhoneLocation()
irontickets_phonelocation_3.Location = u'Home Fax'
irontickets_phonelocation_3.save()
irontickets_phonelocation_4 = PhoneLocation()
irontickets_phonelocation_4.Location = u'Pager'
irontickets_phonelocation_4.save()
irontickets_phonelocation_5 = PhoneLocation()
irontickets_phonelocation_5.Location = u'TDD'
irontickets_phonelocation_5.save()
irontickets_phonelocation_6 = PhoneLocation()
irontickets_phonelocation_6.Location = u'TTY'
irontickets_phonelocation_6.save()
irontickets_phonelocation_7 = PhoneLocation()
irontickets_phonelocation_7.Location = u'Work'
irontickets_phonelocation_7.save()
irontickets_phonelocation_8 = PhoneLocation()
irontickets_phonelocation_8.Location = u'Work Fax'
irontickets_phonelocation_8.save()
