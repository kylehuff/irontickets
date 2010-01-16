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
    Authenticate against a mail server using POP3
    """

    def hunt_for_user(self, user_string):
        usr = None
        user_part = None
        domain_part = None
        try:
            if email_re.search(user_string):
                user_part = user_string.split('@')[0]
                domain_part = user_string.split('@')[1]
                usr = User.objects.get(email=user_string)
            else:
                usr = User.objects.get(username=user_string)
        except User.ObjectNotFound:
            pass
        
        return usr, user_part, domain_part


    def check_pop3s(self, server, port, username, password):
        #TODO: Need to catch the mail server being down and try to auth off cached info in local db
        print 'Attempting to authenticate %s using %s' %(username, server)
        try:
            pop = poplib.POP3_SSL(server, port or 995)
            pop.user(username)
            result = pop.pass_(password)
            pop.quit()
            print result or 'failed!'
            return result
        except:
            return None

    def authenticate(self, username=None, password=None):
        user, user_part, domain_part = self.hunt_for_user(username)
        
        if user:
            prof = user.get_profile()
            company = prof.company
        else:
            prof = None
            company = None

        if user and company.selfsignuphost:
            print 'User exists and selfsignup allowed'
            if company.selfsignupstripdomain:
                try_user = user_part
            else:
                try_user = username
                
            if self.check_pop3s(company.selfsignuphost, int(company.selfsignupport) or 995, try_user, password):
                user.set_password(password)
                user.save()
                print 'login successful'
                return user
            else:
                print 'invalid remote username/password'
                return None
        
        if not user and domain_part:
            print 'user not found, checking domain_part'
            try:
                company = Company.object.get(selfsignupdomain=domain_part)
                print 'company located by domain_part'
            except Company.ObjectNotFound:
                print 'unable to locate company by domain_part'
                return None
            
            if company.allowselfsignup:
                print 'company allows selfsignup'
                if self.check_pop3s(company.selfsignuphost, int(company.selfsignupport) or 995, username, password):
                    print 'login successful'
                    user = User(username=user_part[:25], password=password, email=username)
                    user.set_password(password)
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                    return user
                else:
                    print 'bad remote username/password'
                    return None
            else:
                print 'selfsignup not allowed'
                return None
        return None #We should never get here...


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

