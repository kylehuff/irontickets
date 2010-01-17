from django import forms
from django.forms.util import ErrorList
from django.forms.models import ModelForm, modelformset_factory
from django.forms.widgets import TextInput
from django.forms.forms import Form
from django.forms import ValidationError
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard import FormWizard
from django.contrib.auth.models import User
from irontickets.models import Ticket, TicketStatus, Company, ITProfile, ContactTitle, TechStream
from irontickets.itformwiz import FormWizard


class TechStreamForm(ModelForm):
    error_css_class = 'ui-state-error'
    required_css_class = 'requiredfield'
    
    class Meta:
        model = TechStream
        fields = ('note',)


class TicketForm(ModelForm):
    error_css_class = 'ui-state-error'
    required_css_class = 'requiredfield'
    
    class Meta:
        model = Ticket
        fields = ('company', 'contact', 'status', 'source', 'priority', 'assignedto', 'summary', 'description')


class TicketEditForm(ModelForm):
    error_css_class = 'ui-state-error'
    required_css_class = 'requiredfield'
    
    class Meta:
        model = Ticket
        fields = ('company', 'contact', 'source', 'summary')


class TicketStatusForm(ModelForm):
    error_css_class = 'ui-state-error'
    required_css_class = 'requiredfield'
    
    class Meta:
        model = Ticket
        fields = ('status', 'priority', 'assignedto')


class NewUserForm(forms.Form):
    error_css_class = 'ui-state-error ui'
    required_css_class = 'requiredfield'
    
    Company = forms.ModelChoiceField(queryset = Company.objects.active())
    Title = forms.ModelChoiceField(queryset=ContactTitle.objects.all())
    FirstName = forms.CharField(max_length=30)
    LastName = forms.CharField(max_length=30)
    Email = forms.EmailField()
    JobTitle = forms.CharField(max_length=25)
    Password = forms.CharField(max_length=128,widget=forms.PasswordInput(render_value=False))
    
    def clean_Email(self):
        data = self.cleaned_data['Email']
        if User.objects.filter(email=data):
            raise ValidationError('That e-mail address already exists in the system')
        return data


class CompanyForm(ModelForm):
    error_css_class = 'ui-state-error'
    required_css_class = 'requiredfield'
    
    class Meta:
        model = Company
        fields = ('name', 'type', 'website')

#class NewTicketWizard1(itModelForm):
#	class Meta:
#		model = Ticket
#		fields = ('company')
#	
#class NewTicketWizard2(itModelForm):
#	class Meta:
#		model = Ticket
#		fields = ('contact', 'status', 'source', 'priority', 'assignedto', 'summary', 'description')
#	
#
#class NewTicketWizard(FormWizard):
#	#decorators = [staff_required]
#	def process_step(self, form):
#		pass
#		#if self.step == 0:
#		#	print 
#		#	self.form_list.append(NewTicketWizard2(initial={'contact': self.get_step_data(self.step)['company'].companycontacts_set.all(),}))
#		#elif self.step == 1:
#		#	if is_suburb(form.cleaned_data['company']):
#		#		self.form_list.append(MiddleClassForm)
#
#	def get_template(self):
#		#default = super(NewTicketWizard, self).get_template()
#		default = 'irontickets/tickets/ticket_new.html'
#		template_overrides = {
#			4: "forms/custom_templ.html",
#			5: "forms/custom_templ2.html",
#		}
#		return template_overrides.get(self.step, default)
#
#	def get_form_initial(self, step):
#		if step == 1:
#			return {'contact': self.get_step_data(self.current_request, step - 1)['company'].companycontact_set.all()}
#		return super(NewTicketWizard, self).get_form_initial(step)
#
#	def done(self, final_form_list):
#		"""
#		Create a new customer record.
#		"""
#		print final_form_list

#class CustomerNewTicket1(oiPlainForm):
#	Priority = forms.ModelChoiceField(queryset=TicketPriority.objects.exclude(AvailableInPortal__exact = False), initial='Normal')
#	Summary = forms.CharField(max_length=128, required=True)
#
#class CustomerNewTicket2(oiPlainForm):
#	Description = forms.CharField(widget=forms.Textarea)
#
#
#class CustomerNewTicketWizard(FormWizard):
#	def done(self, request, form_list):
#		tf1 = form_list[0]
#		tf2 = form_list[1]
#
#		newticket = Ticket()
#		newticket.Summary = tf1.cleaned_data['Summary']
#		newticket.Description = tf2.cleaned_data['Description']
#		newticket.Priority = tf1.cleaned_data['Priority']
#		newticket.Contact = request.user
#		newticket.Company = request.user.get_profile().Company
#		newticket.save()
#		return HttpResponseRedirect(reverse('ticketdetail', args=[newticket.pk]))
#
#	def get_template(self, step):
#		return "portal/wizard.html"
#
#
#class SignupForm1(oiPlainForm):
#	Email = forms.EmailField(required=True)
#
#	def clean_Email(self):
#		if User.objects.filter(email__exact=self.cleaned_data['Email']).count() > 0:
#			raise forms.ValidationError('That email address already exists in the system.')
#
#		c = Company.objects.get(EmailDomain__exact=self.cleaned_data['Email'].split('@')[1])
#		if not c.AllowSelfSignup:
#			raise forms.ValidationError('Your email address is not elligible for self-signup.')
#
#		return self.cleaned_data['Email']
#
#	def related_company(self):
#		c = Company.objects.get(EmailDomain__exact=self.cleaned_data['Email'].split('@')[1])
#		return c
#
#class SignupForm2(oiPlainForm):
#	Username = forms.CharField(max_length=25, required=True)
#	Password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())
#
#	def clean_Username(self):
#		if User.objects.filter(username__exact=self.cleaned_data['Username']).count() > 0:
#			raise forms.ValidationError('That Username already exists in the system, please choose a different one')
#		return self.cleaned_data['Username']
#
#class SignupForm3(oiPlainForm):
#	FirstName = forms.CharField(max_length=25, required=True)
#	LastName = forms.CharField(max_length=25, required=True)
#
#class SignupWizard(FormWizard):
#	def done(self, request, form_list):
#		#print self
#		#print request
#		#print form_list
#		sf1 = form_list[0]
#		sf2 = form_list[1]
#		sf3 = form_list[2]
#
#		print "pre create_user"
#		newuser = User.objects.create_user(
#			sf2.cleaned_data['Username'],
#			sf1.cleaned_data['Email'],
#			sf2.cleaned_data['Password']
#		)
#		print "post create_user"
#
#		newuser.first_name = sf3.cleaned_data['FirstName']
#		newuser.last_name = sf3.cleaned_data['LastName']
#		print "pre-save"
#		newuser.save()
#		print "post-save"
#		newprofile = CSProfile(user=newuser)
#		newprofile.Company = sf1.related_company()
#		print "pre profile save"
#		newprofile.save()
#		print "post profile save"
#		return HttpResponseRedirect(reverse('myaccount'))
#
#	def get_template(self, step):
#		return "signup/wizard.html"
#

