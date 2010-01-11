import datetime, sys
from jabberbot import JabberBot, botcmd

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment

from irontickets.models import Ticket

try:
    import xmpp
except ImportError:
    print >>sys.stderr, 'You need to install xmpppy from http://xmpppy.sf.net/.'
    sys.exit(-1)


class Command(BaseCommand):
    help = "Starts the IronTickets Jabber Bot"
    args = '[none]'
    requires_model_validation = True
    
    def handle(self, *args, **options):
        if args:
            raise CommandError('Usage is runserver %s' % self.args)
        
        if not settings.IT_BOT_USERNAME:
            raise CommandError('IT_BOT_USERNAME not specified in settings.py')
        
        if not settings.IT_BOT_PASSWORD:
            raise CommandError('IT_BOT_PASSWORD not specified in settings.py')
        
        quit_command = (sys.platform == 'win32') and 'CTRL-BREAK' or 'CONTROL-C'
        
        def inner_run():
            print "Starting ITBot..."
            bot = ITBot(settings.IT_BOT_USERNAME, settings.IT_BOT_PASSWORD)
            bot.serve_forever()
        try:
            inner_run()
        except KeyboardInterrupt:
            pass

class ITBot(JabberBot):
    def get_name_part(self, jid):
        return str(jid).split('/')[0]

    def unknown_command(self, mess, cmd, args):
        if int(cmd):
            try:
                t = Ticket.objects.get(pk=int(cmd))
                s = "Ticket %s\n" %(t.pk)
                s += "Company: %s\n" %(t.company.name)
                s += "Contact: %s\n" %(t.contact.username)
                s += "Priority: %s\n" %(t.priority)
                s += "Summary: %s\n" %(t.summary)
                s += "Description: %s\n" %(t.description)
                return s
            except Ticket.DoesNotExist:
                return "That ticket number does not exst"
        else:
            return "Unknown command"

# Proposed commands
# list - list of all tickets assigned/open to user
# list u - List all tickets assigned/open to username or email u
# 1 - show ticket 1 info
# 1 x [y] - Add comment to ticket 1, set status to x (or 'x' can be 0 to leave the status
#           unchanged) and add optional comment y
# com 1 - show most recent comment on ticket 1
# asn 1 x - Assign ticket 1 to username or email address x


    @botcmd
    def list(self, mess, args):
        """
            Returns a list of assigned tickets.
            Passing a username or email address returns tickets assigned to that
            user.
        """
        if args:
            user = User.objects.filter(email=args)
        else:
            user = User.objects.get(email=self.get_name_part(mess.getFrom()))
            
        tickets = Ticket.objects.filter(assignedto=user)
        s = ''
        for t in tickets:
            s += 'Ticket %s (%s) - %s\n' %(t.pk, t.company.name, t.summary)
        return s
    
    
    @botcmd
    def com(self, mess, args):
        """Returns the last comment on a ticket"""
        try:
            if int(args):
                t = Ticket.objects.get(pk=args)
                c = Comment.objects.for_model(t).latest('submit_date')
                if c:
                    return "Comment by %s on %s:\n%s\n" %(c.user, c.submit_date, c.comment)
                else:
                    return "No comment for ticket %s" %(args)
        except Ticket.DoesNotExist:
            return "%s is not a valid ticket number" %(args)
        except:
            return "bad input: %s" %(args)

    @botcmd
    def time( self, mess, args):
        """Displays current server time"""
        return str(datetime.datetime.now())
    
    
    @botcmd
    def whoami( self, mess, args):
        """Tells you your username"""
        return self.get_name_part(mess.getFrom())

