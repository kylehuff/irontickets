from django import forms
from django.db import models
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.localflavor.us import models as usmodels
from irontickets.middleware import threadlocals

from datetime import date, timedelta
from time import time

#BUG: Most of the FKs to the User object should actually link to the ITProfile object

class CRUDObject(models.Model):
    created                     = models.DateTimeField(auto_now_add=True)
    createdby                   = models.ForeignKey(User,null=True,blank=True,related_name='%(class)s_createdby_set')
    updated                     = models.DateTimeField(auto_now_add=False, auto_now=True)
    updatedby                   = models.ForeignKey(User,null=True,blank=True,related_name='%(class)s_updatedby_set')

    def save(self):
        if self.pk:
            self.updated        = time()
            self.updatedby      = threadlocals.get_current_user()
        else:
            self.created        = time()
            self.createdby      = threadlocals.get_current_user()
        super(CRUDObject, self).save()

    class Meta:
        abstract = True

class CompanyType(models.Model):
    name                        = models.CharField(max_length=15,primary_key=True)

    def get_absolute_url(self):
        return reverse('company_type_detail', args=[self.id])

    def __unicode__(self):
        return self.name

    class Meta:
        ordering                = ['name']
        verbose_name            = 'Company Type'
        verbose_name_plural     = 'Company Types'


class CompanyStatus(models.Model):
    name                        = models.CharField(max_length=15, primary_key=True)
    active                      = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('company_status_detail', args=[self.id])

    def __unicode__(self):
        return "%s - %s" %(self.active, self.name)

    class Meta:
        ordering                = ['active', 'name']
        verbose_name            = 'Company Status'
        verbose_name_plural     = 'Company Statuses'


class CompanyManager(models.Manager):
    def active(self):
        return self.filter(status__active=True)

    def newthisweek(self):
        weekstart = date.today() + timedelta(-7)
        weekstop = date.today()
        return self.filter(created=weekstart, created__lte=weekstop)


class Company(CRUDObject):
    objects                     = CompanyManager()
    name                        = models.CharField(max_length=30)
    type                        = models.ForeignKey(CompanyType)
    website                     = models.URLField(null=True,blank=True)
    status                      = models.ForeignKey(CompanyStatus, related_name='companystatus_set', default='Active', null=False, blank=False)
    #Agreements
    #Team
    #CompanyEmployees

    def get_absolute_url(self):
        return reverse('companydetail', args=[self.id])

    def __unicode__(self):
        return self.name

    class Meta:
        ordering                = ['name']
        verbose_name            = 'Company'
        verbose_name_plural     = 'Companies'


class ContactTitle(models.Model):
    title                       = models.CharField(max_length=6)

    def __unicode__(self):
        return "%s" %(self.title)

    class Meta:
        ordering                = ['title']
        verbose_name            = 'Contact Title'
        verbose_name_plural     = 'Contact Titles'


class TicketStatus(models.Model):
    name                        = models.CharField(max_length=25,primary_key=True)
    isclosed                    = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('ticketstatusdetail', args=[self.id])

    def __unicode__(self):
        return self.name

    class Meta:
        ordering                = ['name']
        verbose_name            = 'Ticket Status'
        verbose_name_plural     = 'Ticket Statuses'


class TicketSource(models.Model):
    name                        = models.CharField(max_length=25,primary_key=True)

    def get_absolute_url(self):
        return reverse('ticketsourcedetail', args=[self.id])

    def __unicode__(self):
        return "%s" %(self.name)

    class Meta:
        ordering                = ['name']
        verbose_name            = 'Ticket Source'
        verbose_name_plural     = 'Ticket Sources'


class TicketPriority(models.Model):
    name                        = models.CharField(max_length=25,primary_key=True)
    priority                    = models.IntegerField()
    showinportal                = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('ticketprioritydetail', args=[self.id])

    def __unicode__(self):
        return self.name

    class Meta:
        ordering                = ['name']
        verbose_name            = 'Ticket Priority'
        verbose_name_plural     = 'Ticket Priorities'


class TicketManager(models.Manager):
    def open_tickets(self):
        """
        Return a list of open tickets with no children or dupes in the list
        """
        q = Ticket.objects.annotate(n_children = Count('children'))
        return q.filter(status__isclosed=False, n_children=0, duplicateof__exact=None)

    def closed_tickets(self):
        """
        Return a list of closed tickets with no children or dupes in the list
        """
        q = Ticket.objects.annotate(n_children = Count('children'))
        return q.filter(status__isclosed=True, n_children=0, duplicateof__exact=None)

    def assignedthisweek(self):
        weekstart = date.today() + timedelta(-7)
        weekstop = date.today()
        return self.filter(created__gte=weekstart, Created__lte=weekstop)

    def openedthisweek(self):
        weekstart = date.today() + timedelta(-7)
        weekstop = date.today()
        return self.filter(created__gte=weekstart, created__lte=weekstop, status__isclosed=False)

    def closedthisweek(self):
        weekstart = date.today() + timedelta(-7)
        weekstop = date.today()
        return self.filter(created__gte=weekstart, created__lte=weekstop, status__isclosed=True)


class Ticket(CRUDObject):
    objects                     = TicketManager()
    children                    = models.ManyToManyField('self',related_name='parents',blank=True,null=True,symmetrical=False)
    duplicateof                 = models.ForeignKey('self',blank=True,null=True,related_name='duplicate_set')
    company                     = models.ForeignKey(Company, related_name='ticket_set')
    contact                     = models.ForeignKey(User,blank=True,null=True,related_name='ticket_contact_set')
    summary                     = models.CharField(max_length=128)
    description                 = models.TextField()
    status                      = models.ForeignKey(TicketStatus,default='New')
    source                      = models.ForeignKey(TicketSource,default='Website')
    # Agreement
    priority                    = models.ForeignKey(TicketPriority,default='Normal')
    assignedto                  = models.ForeignKey(User,related_name='ticket_assigned_set', null=True, blank=True)
    #InvolvedEquipment
    #InvolvedEmployees
    #InvolvedTasks
    #InvolvedDocuments

    def isChild(self):
        if self.parents.all().count() > 0:
            return True
        return False

    def isDupe(self):
        return self.isDuplicate()

    def isDuplicate(self):
        if not self.duplicateof == None:
            return True
        return False

    def recipient_list(self):
        recipients = []
        if self.assignedto:
            recipients.append(self.assignedto.email)
        if self.contact:
            if self.contact.email:
                recipients.append(self.contact.email)
        return recipients

    def get_absolute_url(self):
        return reverse('ticketdetail', args=[self.id])

    def __unicode__(self):
        return "%s - (%s) - %s" %(self.id, self.company.name, self.summary[:50])

    class Meta:
        ordering                = ['id']
        verbose_name            = 'Ticket'
        verbose_name_plural     = 'Tickets'


class AddressType(models.Model):
    name                        = models.CharField(max_length=8)

    def __unicode__(self):
        return "%s" %(self.name)

    class Meta:
        ordering                = ['name']
        verbose_name            = 'Address Type'
        verbose_name_plural     = 'Address Types'


class Address(CRUDObject):
    contact                     = models.ForeignKey(User)
    type                        = models.ForeignKey(AddressType)
    street                      = models.CharField(max_length=25)
    city                        = models.CharField(max_length=25)
    state                       = usmodels.USStateField()
    zip                         = models.CharField(max_length=10) #TODO: Restrict to ZIP format
    country                     = models.CharField(max_length=15) #TODO: http://www.djangosnippets.org/snippets/1476/

    def __unicode__(self):
        return "%s" %(self.type)

    class Meta:
        ordering                = ['type']
        verbose_name            = 'Address'
        verbose_name_plural     = 'Addresses'


class PhoneLocation(models.Model):
    location                    = models.CharField(max_length=15)

    def __unicode__(self):
        return "%s" %(self.Location)

    class Meta:
        ordering                = ['location']
        verbose_name            = 'Phone Location'
        verbose_name_plural     = 'Phone Locations'


class Phone(CRUDObject):
    contact                     = models.ForeignKey(User)
    location                    = models.ForeignKey(PhoneLocation)
    number                      = usmodels.PhoneNumberField()
    extension                   = models.IntegerField(null=True,blank=True)

    def __unicode__(self):
        if self.Extension:
            return "%s %s x%s" %(self.location, self.number, self.extension)
        else:
            return "%s %s" %(self.Location, self.Number)

    class Meta:
        ordering                = ['location']
        verbose_name            = 'Phone Number'
        verbose_name_plural     = 'Phone Numbers'


class Theme(models.Model):
    theme                       = models.CharField(max_length=25)

    def __unicode__(self):
        return "%s" %(self.theme)
    
    class Meta:
        ordering                = ['theme']


class ITProfile(CRUDObject):
    user                        = models.ForeignKey(User)
    title                       = models.ForeignKey(ContactTitle,null=True,blank=True)
    company                     = models.ForeignKey(Company,null=True,blank=True)
    jobtitle                    = models.CharField(max_length=25,null=True,blank=True)
    notes                       = models.TextField(null=True,blank=True)
    theme                       = models.ForeignKey(Theme,null=True)

    def get_absolute_url(self):
        return reverse('profiledetail', args=[self.id])

    def __unicode__(self):
        return "%s" %(self.user)

    class Meta:
        ordering                = ['user']
        verbose_name            = 'IT Profile'
        verbose_name_plural     = 'IT Profiles'

