"""Business logic for all URLs in the ``gurps_manager`` application."""
from django.core.urlresolvers import reverse
from django import http
from django.shortcuts import render
from django_tables2 import RequestConfig
from django.views.generic.base import View
from gurps_manager import forms, models, tables
import json

# pylint: disable=E1101
# Instance of 'CampaignForm' has no 'is_valid' member (no-member)

class Index(View):
    """Handle a request for ``/``."""
    def get(self, request):
        """Return the homepage for this application."""
        return render(request, 'gurps_manager/index.html', {})

class Campaign(View):
    """Handle a request for ``campaign/``."""
    def post(self, request):
        """Create a new item.

        If creation succeeds, rediret user to ``CampaignId`` view. Otherwise,
        redirect user to ``CampaignCreateForm`` view.

        """
        form = forms.CampaignForm(request.POST)
        if form.is_valid():
            new_campaign = form.save()
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-campaign-id',
                args = [new_campaign.id]
            ))
        else:
            # Put form data into session. Destination view will use it.
            request.session['form_data'] = json.dumps(form.data)
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-create-form'
            ))

    def get(self, request):
        """Return a list of all campaigns."""
        table = tables.CampaignTable(models.Campaign.objects.all())
        RequestConfig(request).configure(table)
        return render(
            request,
            'gurps_manager/campaign.html',
            {'table': table, 'request': request}
        )

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
