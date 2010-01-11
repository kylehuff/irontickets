from django.conf import settings
from django.db.models.signals import pre_save
from django.template import loader, Context
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site
from mailer import send_mail
from irontickets.models import Ticket

#pre_save
#django.db.models.signals.pre_save
#sender    The model class.
#instance    The actual instance being saved.

def fieldcmp(changes, oldfield, newfield, text):
    if oldfield != newfield:
        changes.append('%s: %s => %s' %(text, oldfield, newfield))
    return changes


def ticket_pre_save(sender, instance, **kwargs):
    print "SIGNAL ticket_pre_save:", sender, instance, kwargs

    if not Ticket.objects.filter(pk=instance.pk):
        return

    print "signal changed ticket"
    template = loader.get_template('irontickets/email/ticket_update.txt')
    subjecttemplate = loader.get_template('irontickets/email/ticket_update_subject.txt')
    old = Ticket.objects.get(pk=instance.pk)
    #BUG: If the ticket is marked as a dupe we only need to send an email saying the ticket has been flagged as a dupe with a link to the new ticket
    #BUG: If the ticket children have changed, we need to send out notifications to all the children
    changelist = []
    changelist = fieldcmp(changelist, old.company, instance.company, 'Company')
    changelist = fieldcmp(changelist, old.contact, instance.contact, 'Contact')
    changelist = fieldcmp(changelist, old.summary, instance.summary, 'Summary')
    changelist = fieldcmp(changelist, old.status, instance.status, 'Status')
    changelist = fieldcmp(changelist, old.priority, instance.priority, 'Priority')
    changelist = fieldcmp(changelist, old.source, instance.source, 'Source')
    changelist = fieldcmp(changelist, old.assignedto, instance.assignedto, 'Assigned to')
    changelist = fieldcmp(changelist, old.description, instance.description, 'Description')
    if not changelist:
        return

    current_site = Site.objects.get_current()

    context = Context({
        'ticket': instance,
        'change_list': changelist,
        'site': current_site,
        'proto': settings.IT_USE_PROTO,
    })
    
    subject = subjecttemplate.render(context)
    message = template.render(context)
    
    recipients = instance.recipient_list()
    
    #BUG: fail_silently should be True in production
    send_mail(subject, message, 'ticket+%s@irontickets.com' %(instance.pk), recipients, fail_silently=False)


def ticket_post_save(sender, instance, **kwargs):
    print "SIGNAL ticket_post_save:", sender, instance, kwargs

    if not kwargs.get('created', False):
        return
        
    print "signal new ticket %s" %(instance.pk)
    template = loader.get_template('irontickets/email/ticket_new.txt')
    subjecttemplate = loader.get_template('irontickets/email/ticket_new_subject.txt')
    
    current_site = Site.objects.get_current()

    context = Context({
        'ticket': instance,
        'site': current_site,
        'proto': settings.IT_USE_PROTO,
    })
    
    subject = subjecttemplate.render(context)
    message = template.render(context)
    
    recipients = instance.recipient_list()
    
    #BUG: fail_silently should be True in production
    send_mail(subject, message, 'ticket+%s@irontickets.com' %(instance.pk), recipients, fail_silently=False)


def comment_post_save(sender, instance, **kwargs):
    return #BUG: Unfinished


    print "SIGNAL comment_post_save:", sender, instance, kwargs

#    if not kwargs.get('created', False):
#        return
        
    print "signal new comment %s" %(instance.pk)

    template = loader.get_template('irontickets/email/ticket_comment_new.txt')
    subjecttemplate = loader.get_template('irontickets/email/ticket_comment_new_subject.txt')

    current_site = Site.objects.get_current()
    
    #BUG: Docs say this should return the ticket object, but it returns None.
    ticket = instance.content_object

    context = Context({
        'comment': instance,
        'ticket': ticket,
        'site': current_site,
        'proto': settings.IT_USE_PROTO,
    })
    
    subject = subjecttemplate.render(context)
    message = template.render(context)
    
    recipients = instance.recipient_list()
    
    #BUG: fail_silently should be True in production
    send_mail(subject, message, 'ticket+%s@irontickets.com' %(instance.pk), recipients, fail_silently=False)

