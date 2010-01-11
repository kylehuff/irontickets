#!/usr/bin/python

import email, imaplib, mimetypes, poplib, os, re

from datetime import datetime, timedelta
from email.header import decode_header
from email.Utils import parseaddr, getaddresses
from optparse import make_option
from tempfile import mkstemp

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from irontickets.models import Ticket, TicketPriority, TicketSource, Company
from attachments.models import Attachment

class Command(BaseCommand):
    def __init__(self):
        BaseCommand.__init__(self)

        self.option_list += (
            make_option(
                '--quiet', '-q',
                default=False,
                action='store_true',
                help='Hide details about each message as it is processed'),
            )
    help = 'Suck e-mail into IronTickets via POP3 and/or IMAP.'

    def handle(self, *args, **options):
        quiet = options.get('quiet', False)
        if not settings.IT_MAILSUCK_SERVER_TYPE:
            raise CommandError('IT_MAILSUCK_SERVER_TYPE not specified in settings.py')
        if not settings.IT_MAILSUCK_SERVER:
            raise CommandError('IT_MAILSUCK_SERVER not specified in settings.py')
        if not settings.IT_MAILSUCK_USER:
            raise CommandError('IT_MAILSUCK_USER not specified in settings.py')
        if not settings.IT_MAILSUCK_PASS:
            raise CommandError('IT_MAILSUCK_PASS not specified in settings.py')
        fetch_mail(settings.IT_MAILSUCK_SERVER_TYPE, settings.IT_MAILSUCK_SERVER, settings.IT_MAILSUCK_USER, settings.IT_MAILSUCK_PASS)


def fetch_mail(server_type, server_name, server_user, server_pass):
    if server_type == 'pop3':
        server = poplib.POP3(server_name, 110)
    
    if server_type == 'pop3s':
        server = poplib.POP3_SSL(server_name, 995)
    
    if server_type == 'imap':
        server = imaplib.IMAP4(server_name, 143)
    
    if server_type == 'imaps':
        server = imaplib.IMAP4_SSL(server_name, 993)
    
    if not server:
        raise CommandError('Unknown IT_MAILSUCK_SERVER_TYPE: %s' %(server_type))

    if 'pop3' in server_type:
        server.getwelcome()
        server.user(server_user)
        server.pass_(server_pass)
        messages = server.list()[1]
        for message in messages:
            print message.split('.')
            msgnum, msgsize = message.split('.')
            msg = server.retr(msgnum)[1]
            #print "Message retrieved: %s" %(msg)
            t = ticket_from_message(msg)
            if t:
                server.dele(msgnum)
        server.quit()
    else:
        print "Logging in to IMAP server"
        server.login(server_user, server_pass)
        print "Opening inbox..."
        server.select()
        while True:
            print "Fetching messages"
            status, data = server.search(None, 'NOT', 'DELETED')
            message_count = data[0].split()
            if not message_count:
                break
            for msgnum in message_count:
                status, data = server.fetch(msgnum, '(RFC822)')
                t = ticket_from_message(data[0][1])
                if t:
                    server.store(msgnum, '+FLAGS', '\\Deleted')
        
        server.expunge()
        server.close()
        server.logout()


def decodeUnknown(charset, string):
    if not charset:
        try:
            string = string.decode('utf-8')
        except:
            string = string.decode('iso8859-1')
    string = unicode(string)
    return string

def get_address_parts(address):
    """
    acceps one email address as returned from getaddresses and
    spits the address back in an array of the following parts
    name
    user part (minus plus part if any)
    plus part (None if no plus part)
    domain part
    """
    data = []
    data.append(address[0]) #Name
    user = address[1].split('@')[0] #User part
    plus = None
    if '+' in user:
        data.append(user.split('+')[0]) #Cleaned user part
        data.append(user.split('+')[1]) #Plus part
    else:
        data.append(user) #User part
        data.append(None) #No plus part
    data.append(address[1].split('@')[1]) #Domain part
    return data


def ticket_from_message(message):
    # 'message' must be an RFC822 formatted message.
    
    #BUG: We need to check for messages address to multiple tickets
    #BUG: Don't break with multiple 'to' addresses
    #BUG: What if a ticket is CC'd?
    
    message = email.message_from_string(message)
    subject = message.get('subject', 'No Subject')
    subject = subject.replace('Re:', '')
    subject = subject.replace('RE:', '')
    subject = subject.replace('re:', '')
    subject = subject.replace('FW:', '')
    subject = subject.replace('Fw:', '')
    subject = subject.replace('fw:', '')
    subject = subject.strip()

    sender = message.get('from', None)
    sender_email = parseaddr(sender)[1]

    recipients = getaddresses(message.get_all('to', []) + message.get_all('cc', []))
    #TODO: Check if all recipients are associated with the ticket(s), add if not
    
    tickets = []
    for recipient in recipients:
        name_part, user_part, plus_part, domain_part = get_address_parts(recipient)
        if user_part + '@' + domain_part == settings.IT_MAILSUCK_ADDRESS:
            #This recipient is a ticket address
            print 'Message destined for ticket system'
            if plus_part:
                #Message is destined for a specific ticket
                print 'Message allegedly for ticket: %s' %(plus_part)
                try:
                    t = Ticket.objects.get(pk=plus_part)
                    print 'Ticket found %s' %(plus_part)
                    if not t in tickets:
                        tickets.append(t)
                except Ticket.ObjectNotFound:
                    print 'Unable to locate ticket %s' %(plus_part)
                    continue
                    #BUG: This should be logged (in fact, all incoming messages should be logged...)
            else:
                t = Ticket()
                if not t in tickets:
                    tickets.append(t)
        else:
            print 'Not destined for ticket system, skipping' %(recipient)
            continue

#BUG: Don't blindly accept mail/attachments for existing tickets.  Allow only from people involved with the ticket.
#BUG: Don't blindly create new tickets, check account status

    body_plain, body_html = '', ''
    counter = 0
    files = []
    for part in message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        
        print 'Part params: '
        print part.get_params()
        name = part.get_param('name')

        if part.get_content_maintype() == 'text' and name == None:
            if part.get_content_subtype() == 'plain':
                body_plain = decodeUnknown(part.get_charset(), part.get_payload(decode=True))
            else:
                body_html = part.get_payload(decode=True)
        else:
            if not name:
                name = part.get_filename()
            
            files.append({
                'filename': name,
                'content': part.get_payload(decode=True),
                'type': part.get_content_type()},
                )
        counter += 1

    if body_plain:
        body = body_plain
    else:
        body = 'No plain-text email body available. Please see HTML attachment.'

    if body_html:
        files.append({
            'filename': 'email_html_body.html',
            'content': body_html,
            'type': 'text/html',
        })
    now = datetime.now()

    for ticket in tickets:
        if ticket.pk:
            #TODO: Existing tickets need a comment created
            pass
        else:
            #TODO: Lookup contact by e-mail, find associated company
            ticket.company = Company.objects.get(pk=1) #BUG: Hardcoded
            ticket.contact = User.objects.get(pk=1) #BUG: Hardcoded
            #TODO: Need to have finish 'team' setup and have a default tech for each account
            ticket.assignedto = User.objects.get(pk=1)
            ticket.source = TicketSource.objects.get(pk='E-Mail')
            ticket.summary =  subject
            ticket.description = body

        important_types = ('high', 'important', '1', 'urgent')
        if message.get('priority', '') in important_types or message.get('importance', '') in important_types:
            ticket.priority = TicketPriority.objects.get(name='Emergency')
        else:
            ticket.priority = TicketPriority.objects.get(name='Normal')

        #TODO: Check ticket status, change appropriately
        #TODO: Make sure everyone in 'to' or 'cc' get included in the ticket notification list

        #Save the ticket before attaching files...
        print ticket
        ticket.save()
    
    for file in files:
        print "Scanning through attachments"
        if file['content']:
            print 'Attaching file: %s' %(file['filename'])
            filename = file['filename'].encode('ascii', 'replace').replace(' ', '_')
            filename = re.sub('[^a-zA-Z0-9._-]+', '', filename)

            print 'Almost there: %s' %(filename)
            fh, fpath = mkstemp(prefix='itmailattach-', suffix='-%s' %(filename), text=True)
            f = open(fpath, 'w+')
            print 'Writing attachment to %s' %(fpath)
            f.write(file['content'])
            f.flush()
            fa = File(open(fpath, 'r'))

            for ticket in tickets:
                a = Attachment()
                a.content_object = ticket
                a.creator = User.objects.get(pk=1) #BUG: We need a way to specify a 'system' user or something
                a.attachment_file = fa
                a.save()

            fa.close()
            f.close()
            os.remove(fpath)

    return True


if __name__ == '__main__':
    fetch_mail()


