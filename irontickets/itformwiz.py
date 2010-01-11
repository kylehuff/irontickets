from django.shortcuts import render_to_response
from django.template.context import RequestContext

class FormWizard(object):
    """
    FormWizard class -- implements a multi-page form, validating between each
    step and storing the form's state in the current session.
    """
    # Dictionary of extra template context variables.
    extra_context = {}

    # List of decorators to be applied to the __call__ "view"
    decorators = []

    # The key to use when storing and retrieving form data from the session.
    data_session_key = "wizard_data"

    # The key to use when storing and retrieving context data from the session.
    context_session_key = "wizard_extra_context"

    # The key to use when storing and retrieving the current step from the session.
    step_session_key = "wizard_step"

    # Methods that subclasses shouldn't need to override #######################

    def __init__(self, form_list):
        "form_list should be a list of Form classes (not instances)."
        self.form_list = form_list[:]
        self.step = 0 # A zero-based counter keeping track of which step we're in.
        for dec in self.decorators[::-1]:
            self.__call__ = dec(self.__call__)
    def __repr__(self):
        return "step: %d\nform_list: %s\ninitial_data: %s" % (self.step, self.form_list, self.initial)

    def get_form(self, step=None, data=None):
        "Helper method that returns the Form instance for the given step."
        if step is None:
            step = self.step
        return self.form_list[step](data=data, prefix=self.get_form_prefix(step), initial=self.get_form_initial(step))

    def _num_steps(self):
        # You might think we should just set "self.num_steps = len(form_list)"
        # in __init__(), but this calculation needs to be dynamic, because some
        # hook methods might alter self.form_list.
        return len(self.form_list)
    num_steps = property(_num_steps)

    def __call__(self, request, *args, **kwargs):
        """
        Main method that does all the hard work, conforming to the Django view
        interface.
        """
        self.current_request = request
        if 'extra_context' in kwargs:
            self.extra_context.update(kwargs['extra_context'])
        self.step = self.determine_step(*args, **kwargs)
        self.parse_params(*args, **kwargs)

        # GET requests automatically start the FormWizard at the first form.
        if request.method == 'GET':
            self.reset_wizard()
            form = self.get_form()
            return self.render(form)
        else:
            form = self.get_form(data=request.POST)
            self.extra_context.update(self.current_request.session.get(self.context_session_key,{}))
            if form.is_valid():
                self.step_data = form.cleaned_data
                self.process_step(form)
                self.store_step_data()
                self.store_extra_context()
                next_step = self.step + 1

                # If this was the last step, validate all of the forms one more
                # time, as a sanity check, and call done().
                if next_step == self.num_steps:
                    final_form_list = []
                    # Validate all the forms. If any of them fail validation, that
                    # must mean something like self.process_step(form) modified
                    # self.step_data after it was validated.
                    for i in range(self.num_steps):
                        frm = self.get_form(step=i, data=request.session.get(self.data_session_key, {}))
                        if not frm.is_valid():
                            return self.render_revalidation_failure(step, frm)
                        final_form_list.append(frm)
                    final_form_list.append(form)
                    return self.done(final_form_list)
                # Otherwise, move along to the next step.
                else:
                    new_form = self.get_form(next_step)
                    self.store_step(next_step)
                    return self.render(new_form)
            # Form is invalid, render it with errors.
            return self.render(form)

    def render(self, form):
        "Renders the given Form object, returning an HttpResponse."
        return self.render_template(form)

    def reset_wizard(self):
        try:
            del(self.current_request.session[self.data_session_key])
        except:
            pass
        self.current_request.session.modified = True
        self.store_step(0)

    # METHODS SUBCLASSES MIGHT OVERRIDE IF APPROPRIATE ########################

    def get_form_prefix(self, step=None):
        "Returns a Form prefix to use."
        if step is None:
            step = self.step
        return str(step)

    def get_form_initial(self, step):
        "Returns the value to pass as the 'initial' keyword argument to the Form class."
        return None

    def store_extra_context(self):
        """
        Stores self.extra_context to the session.  Note that this means
        extra_context is global across all steps of the Wizard.  You can
        redefine a context variable "author" to mean two different things in
        different steps, but you don't get your first one back once you've
        overwritten it.  This can affect your ability to assign to self.step.
        """
        self.current_request.session[self.context_session_key] = self.extra_context
        self.current_request.session.modified = True

    def get_step_data(self, request, step):
        "Retrieves data for the specified step"
        return request.session[self.data_session_key][step]

    def store_step_data(self, step=None, data=None):
        if step is None:
            step = self.step
        if data is None:
            data = self.step_data
        if self.data_session_key not in self.current_request.session:
            self.current_request.session[self.data_session_key] = {step:data}
        else:
            self.current_request.session[self.data_session_key][step] = data
        self.current_request.session.modified=True

    def store_step(self, step=None):
        if step is not None:
            self.step = step
        self.current_request.session[self.step_session_key] = self.step
        self.current_request.session.modified = True

    def render_revalidation_failure(self, step, form):
        """
        Hook for rendering a template if final revalidation failed.

        It is highly unlikely that this point would ever be reached, but see
        the comment in __call__() for an explanation.
        """
        return self.render(form)

    def determine_step(self, *args, **kwargs):
        """
        Given the request object and whatever *args and **kwargs were passed to
        __call__(), returns the current step (which is zero-based).
        """
        return self.current_request.session.get(self.step_session_key, 0)

    def parse_params(self, *args, **kwargs):
        """
        Hook for setting some state, given the request object and whatever
        *args and **kwargs were passed to __call__(), sets some state.

        This is called at the beginning of __call__().
        """
        pass

    def get_template(self):
        """
        Hook for specifying the name of the template to use for a given step.

        Note that this can return a tuple of template names if you'd like to
        use the template system's select_template() hook.
        """
        return 'forms/wizard.html'

    def render_template(self, form=None):
        """
        Renders the template for the current step, returning an HttpResponse object.

        Override this method if you want to add a custom context, return a
        different MIME type, etc. If you only need to override the template
        name, use get_template() instead.

        The template will be rendered with the following context:
            step       -- The current step (one-based).
            step0      -- The current step (zero-based).
            step_count -- The total number of steps.
            form       -- The Form instance for the current step (either empty
                          or with errors).
        """
        form = form or self.get_form()
        return render_to_response(self.get_template(), dict(
            self.extra_context,
            step=self.step+1,
            step0=self.step,
            step_count=self.num_steps,
            form=form,
        ), context_instance=RequestContext(self.current_request))

    def process_step(self, form):
        """
        Hook for modifying the FormWizard's internal state, given a fully
        validated Form object. The Form is guaranteed to have clean, valid
        data.  This method is where you could assign things to self.extra_context,
        self.current_request, or self.step_data.

        Assign a dict-like object to self.step_data to override the data being
        stored for the current step.  self.step_data is set to form.cleaned_data
        by default.
        """
        pass

    # METHODS SUBCLASSES MUST OVERRIDE ########################################

    def done(self, form_list):
        """
        Hook for doing something with the validated data. This is responsible
        for the final processing.

        form_list is a list of Form instances, each containing clean, valid
        data.
        """
        raise NotImplementedError("Your %s class has not defined a done() method, which is required." % self.__class__.__name__)
