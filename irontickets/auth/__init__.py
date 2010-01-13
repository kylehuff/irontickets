from django.conf import settings
from django.contrib.auth.models import User, check_password
from django.core.validators import email_re
from irontickets.models import Company, ITProfile
import poplib

# Self-signup types from models.py
#    (1, 'POP3'),
#    (2, 'POP3-TLS'),
#    (3, 'POP3S'),
#    (4, 'IMAP'),
#    (5, 'IMAP-TLS'),
#    (6, 'IMAP-SSL'),


class POP3Backend:
    """
    Authenticate against a mail server via POP3+TLS
    """

    def authenticate(self, username=None, password=None):
        if not email_re.search(username):
            return None
        
        user_part = username.split('@')[0]
        domain_part = username.split('@')[1]
        
        try:
            usr = User.objects.get(email=username)
        except User.ObjectNotFound:
            print 'User not found via e-mail address'
            return None
        
        if not usr:
            try:
                company = Company.objects.get(selfsignupdomain=domain_part)
                print 'located company record by domain_part'
            except Company.ObjectNotFound:
                print 'Unable to locate company by domain part %s' %(domain_part)
                return None
        
        if usr:
            try:
                prof = usr.get_profile()
            except:
                print 'Unable to get profile for username %s' %(username)
            
            try:
                company = prof.company
            except:
                print 'Unable to jump from profile to company for username %s' %(username)
                return None
        else:
            return None
            #BUG: Handle a user without a profile by checking domain_part
        
        print 'Ready for auth with:'
        print user_part, domain_part
        print usr, prof, company

        #TODO: Need to catch the mail server being down and try to auth off cached info in local db
        pop = poplib.POP3_SSL(company.selfsignuphost, port=int(company.selfsignupport) or 995)
        if company.selfsignupstripdomain:
            print 'Trying to auth as %s' %(user_part)
            pop.user(user_part)
        else:
            print 'Trying to auth as %s' %(username)
            pop.user(username)
        
        result = pop.pass_(password)
        pop.quit()

        if result:
            print result
            login_valid = True
        else:
            print "failed"
            login_valid = False

        if login_valid:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                user = User(username=username[:25], password=password, email=username)
                user.is_staff = False
                user.is_superuser = False
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

