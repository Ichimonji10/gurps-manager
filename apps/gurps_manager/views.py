"""Business logic for all URLs in the ``gurps_manager`` application."""
from django.shortcuts import render
from django.views.generic.base import View
from gurps_manager import forms

class Index(View):
    """Handle a request for ``/``."""
    def get(self, request):
        """Return the homepage for this application."""
        return render(request, 'gurps_manager/index.html', {})

class Campaign(View):
    pass

class CampaignCreateForm(View):
    """Handle a request for ``campaign/create-form/``."""
    def get(self, request):
        """Return a form for creating a campaign."""
        form_data = request.session.pop('form_data', None)
        if form_data is None:
            form = forms.CampaignForm()
        else:
            form = forms.CampaignForm(json.loads(form_data))
        return render(
            request,
            'gurps_manager/campaign-create-form.html',
            {'form': form}
        )
