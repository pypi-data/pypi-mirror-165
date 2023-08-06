
from allauth.account.forms import LoginForm

class DwllLoginForm(LoginForm):

    def login(self, *args, **kwargs):

        # Add your own processing here.

        # You must return the original result.
        return super(DwllLoginForm, self).login(*args, **kwargs)