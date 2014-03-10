"""Business logic for all URLs in the ``gurps_manager`` application."""
from django.contrib import auth
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.urlresolvers import reverse
from django import http
from django.shortcuts import render
from django_tables2 import RequestConfig
from django.views.generic.base import View
from gurps_manager import forms, models, tables
import json

# pylint: disable=E1101
# Instance of 'CampaignForm' has no 'is_valid' member (no-member)
# pylint: disable=R0201
# Framework requires use of methods rather than functions

class Index(View):
    """Handle a request for ``/``."""
    def get(self, request):
        """Return the homepage for this application."""
        return render(request, 'gurps_manager/index.html', {})

class Login(View):
    """Handle a request for ``login/``."""
    def get(self, request):
        """Return a form for logging in."""
        form_data = request.session.pop('form_data', None)
        if form_data is None:
            form = forms.LoginForm()
        else:
            form = forms.LoginForm(json.loads(form_data))
        return render(request, 'gurps_manager/login.html', {'form': form})

    def post(self, request):
        """Log in user.

        If login suceeds, redirect user to ``index`` view. Otherwise, redirect
        user to ``login`` view.

        """
        # Check validity of submitted data
        form = forms.LoginForm(request.POST)
        if not form.is_valid():
            request.session['form_data'] = json.dumps(form.data)
            return http.HttpResponseRedirect(reverse('gurps-manager-login'))

        # Check for invalid credentials.
        user = auth.authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user is None:
            form._errors[NON_FIELD_ERRORS] = form.error_class([
                'Credentials are invalid.'
            ])
            request.session['form_data'] = json.dumps(form.data)
            return http.HttpResponseRedirect(reverse('gurps-manager-login'))

        # Check for inactive user
        if not user.is_active:
            form._errors[NON_FIELD_ERRORS] = form.error_class([
                'Account is inactive.'
            ])
            request.session['form_data'] = json.dumps(form.data)
            return http.HttpResponseRedirect(reverse('gurps-manager-login'))

        # Everything checks out. Let 'em in.
        auth.login(request, user)
        return http.HttpResponseRedirect(reverse('gurps-manager-index'))

    def delete(self, request):
        """Log out user.

        Redirect user to ``login`` after logging out user.

        """
        auth.logout(request)
        return http.HttpResponseRedirect(reverse('gurps-manager-login'))

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
                args=[new_campaign.id]
            ))
        else:
            # Put form data into session. Destination view will use it.
            request.session['form_data'] = json.dumps(form.data)
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-campaign-create-form'
            ))

    def get(self, request):
        """Return a list of all campaigns."""
        table = tables.CampaignTable(models.Campaign.objects.all())
        RequestConfig(request).configure(table)
        return render(
            request,
            'gurps_manager/campaign_templates/campaign.html',
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
            'gurps_manager/campaign_templates/campaign-create-form.html',
            {'form': form}
        )

class CampaignId(View):
    """Handle a request for ``campaign/<id>/``."""
    def get(self, request, campaign_id):
        """Return information about campaign ``campaign_id``."""
        campaign = _get_model_object_or_404(models.Campaign, campaign_id)
        return render(
            request,
            'gurps_manager/campaign_templates/campaign-id.html',
            {'campaign': campaign}
        )

    def put(self, request, campaign_id):
        """Update campaign ``campaign_id``.

        If update suceeds, redirect user to ``CampaignId`` view. Otherwise,
        redirect user to ``CampaignIdUpdateForm`` view.

        """
        campaign = _get_model_object_or_404(models.Campaign, campaign_id)
        form = forms.CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-campaign-id',
                args=[campaign_id]
            ))
        else:
            request.session['form_data'] = json.dumps(form.data)
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-campaign-id-update-form',
                args=[campaign_id]
            ))

    def delete(self, request, campaign_id): #pylint: disable=W0613
        """Delete campaign ``campaign_id``.

        After delete, redirect user to ``Campaign`` view.

        """
        _get_model_object_or_404(models.Campaign, campaign_id).delete()
        return http.HttpResponseRedirect(reverse('gurps-manager-campaign'))

    def dispatch(self, request, *args, **kwargs):
        """Override normal method dispatching behaviour."""
        request.method = _decode_request(request)
        return super().dispatch(request, *args, **kwargs)

class CampaignIdUpdateForm(View):
    """Handle a request for ``campaign/<id>/update-form``."""
    def get(self, request, campaign_id):
        """Return a form for updating campaign ``campaign_id``."""
        campaign = _get_model_object_or_404(models.Campaign, campaign_id)
        form_data = request.session.pop('form_data', None)
        if form_data is None:
            form = forms.CampaignForm(instance=campaign)
        else:
            form = forms.CampaignForm(json.loads(form_data))
        return render(
            request,
            'gurps_manager/campaign_templates/campaign-id-update-form.html',
            {'campaign': campaign, 'form': form}
        )

class CampaignIdDeleteForm(View):
    """Handle a request for ``campaign/<id>/delete-form``."""
    def get(self, request, campaign_id):
        """Return a form for deleting campaign ``campaign_id``."""
        campaign = _get_model_object_or_404(models.Campaign, campaign_id)
        return render(
            request,
            'gurps_manager/campaign_templates/campaign-id-delete-form.html',
            {'campaign': campaign}
        )

class Character(View):
    """Handle a request for ``character/``."""
    def post(self, request):
        """Create a new item.

        If creation succeeds, rediret user to ``CharacterId`` view. Otherwise,
        redirect user to ``CharacterCreateForm`` view.

        """
        form = forms.CharacterForm(request.POST)
        if form.is_valid():
            new_character = form.save()
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-character-id',
                args=[new_character.id]
            ))
        else:
            # Put form data into session. Destination view will use it.
            request.session['form_data'] = json.dumps(form.data)
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-character-create-form'
            ))

    def get(self, request):
        """Return a list of all characters."""
        table = tables.CharacterTable(models.Character.objects.all())
        RequestConfig(request).configure(table)
        return render(
            request,
            'gurps_manager/character_templates/character.html',
            {'table': table, 'request': request}
        )

class CharacterId(View):
    """Handle a request for ``character/<id>/``."""
    def get(self, request, character_id):
        """Return information about character ``character_id``."""
        character = _get_model_object_or_404(models.Character, character_id)
        return render(
            request,
            'gurps_manager/character_templates/character-id.html',
            {'character': character}
        )

    def put(self, request, character_id):
        """Update character ``character_id``.

        If update suceeds, redirect user to ``CharacterId`` view. Otherwise,
        redirect user to ``CharacterIdUpdateForm`` view.

        """
        # Does the requested character exist, and is the user authorized to
        # update this character?
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden()

        # Attempt to update the character.
        form = forms.CharacterForm(request.POST, instance=character)
        if form.is_valid():
            form.save()
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-character-id',
                args=[character_id]
            ))
        else:
            request.session['form_data'] = json.dumps(form.data)
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-character-id-update-form',
                args=[character_id]
            ))

    def delete(self, request, character_id): #pylint: disable=W0613
        """Delete character ``character_id``.

        After delete, redirect user to ``Character`` view.

        """
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden()
        character.delete()
        return http.HttpResponseRedirect(reverse('gurps-manager-character'))

    def dispatch(self, request, *args, **kwargs):
        """Override normal method dispatching behaviour."""
        request.method = _decode_request(request)
        return super().dispatch(request, *args, **kwargs)

class CharacterCreateForm(View):
    """Handle a request for ``character/create-form/``."""
    def get(self, request):
        """Return a form for creating a character."""
        form_data = request.session.pop('form_data', None)
        if form_data is None:
            form = forms.CharacterForm()
        else:
            form = forms.CharacterForm(json.loads(form_data))
        return render(
            request,
            'gurps_manager/character_templates/character-create-form.html',
            {'form': form}
        )

class CharacterIdUpdateForm(View):
    """Handle a request for ``character/<id>/update-form``."""
    def get(self, request, character_id):
        """Return a form for updating character ``character_id``."""
        # Does the requested character exist, and is the user authorized to
        # update this character?
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden('Error: you do not own this character.')

        # Populate and return an update form.
        form_data = request.session.pop('form_data', None)
        if form_data is None:
            form = forms.CharacterForm(instance=character)
        else:
            form = forms.CharacterForm(json.loads(form_data))
        return render(
            request,
            'gurps_manager/character_templates/character-id-update-form.html',
            {'character': character, 'form': form}
        )

class CharacterIdDeleteForm(View):
    """Handle a request for ``character/<id>/delete-form``."""
    def get(self, request, character_id):
        """Return a form for deleting character ``character_id``."""
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden('Error: you do not own this character.')
        return render(
            request,
            'gurps_manager/character_templates/character-id-delete-form.html',
            {'character': character}
        )

def _decode_request(request):
    """Determine what HTTP method ``request.method`` represents.

    ``request`` is a ``django.http.HttpRequest`` object.

    If ``request`` is an HTTP POST request and the query string contains key
    '_method', return the corresponding query string value. This allows clients
    (especially web browsers) to submit HTTP POST requests which emulate other
    HTTP request types, such as PUT and DELETE.

    >>> class FakeRequest(object):
    ...     def __init__(self, method, post_dict):
    ...         self.method = method
    ...         self.POST = post_dict
    >>> _decode_request(FakeRequest('POST', {'_method': 'PUT'}))
    'PUT'
    >>> _decode_request(FakeRequest('POST', {'_method': 'foo'}))
    'foo'
    >>> _decode_request(FakeRequest('GET', {'_method': 'foo'}))
    'GET'

    """
    if 'POST' == request.method:
        return request.POST.get('_method', 'POST')
    return request.method

def _get_model_object_or_404(model, object_id):
    """Return an object of type ``model`` with ID ``object_id``.

    ``model`` is a model class. (Class ``model`` is probably defined in file
    ``models.py``.) ``object_id`` is the ID of one of those objects.

    If an object with ID ``object_id`` cannot be found, raise exception
    ``django.http.Http404``.

    >>> from django.http import Http404
    >>> from gurps_manager import factories, models
    >>> campaign = factories.CampaignFactory.create()
    >>> campaign2 = _get_model_object_or_404(models.Campaign, campaign.id)
    >>> campaign == campaign2
    True
    >>> try:
    ...     _get_model_object_or_404(models.Campaign, campaign.id + 1)
    ... except Http404:
    ...     'an exception was raised'
    'an exception was raised'

    """
    try:
        return model.objects.get(id=object_id)
    except model.DoesNotExist:
        raise http.Http404

def _user_owns_character(user, character):
    """Check whether ``user`` owns ``character``, directly or indirectly.

    Return ``True`` if ``user`` owns ``character``, or if ``user`` owns the
    campaign to which ``character`` belongs. Else, return ``False``.

    >>> from gurps_manager import factories
    >>> character = factories.CharacterFactory.create()
    >>> _user_owns_character(character.owner, character)
    True
    >>> _user_owns_character(character.campaign.owner, character)
    True
    >>> other_user = factories.UserFactory.create()
    >>> _user_owns_character(other_user, character)
    False

    """
    if character.owner == user or character.campaign.owner == user:
        return True
    return False
