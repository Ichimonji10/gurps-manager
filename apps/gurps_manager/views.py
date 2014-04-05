"""Business logic for all URLs in the ``gurps_manager`` application."""
from django.contrib import auth
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.urlresolvers import reverse
from django.db.models import Q
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
        """Return a list of all campaigns viewable by a user."""
        campaigns = _viewable_campaigns(request.user)
        campaign_table_cls = tables.campaign_table(request.user)
        table = campaign_table_cls(campaigns)
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
        if campaign not in _viewable_campaigns(request.user):
            return http.HttpResponseForbidden(
                'Error: you do not have the rights to view this campaign.'
            )
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
        if not _user_owns_campaign(request.user, campaign):
            return http.HttpResponseForbidden(
                'Error: you do not own this campaign.'
            )
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
        campaign = _get_model_object_or_404(models.Campaign, campaign_id)
        if not _user_owns_campaign(request.user, campaign):
            return http.HttpResponseForbidden(
                'Error: you do not own this campaign.'
            )
        campaign.delete()
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
        if not _user_owns_campaign(request.user, campaign):
            return http.HttpResponseForbidden(
                'Error: you do not own this campaign.'
            )
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
        if not _user_owns_campaign(request.user, campaign):
            return http.HttpResponseForbidden(
                'Error: you do not own this campaign.'
            )
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
        """Return information about several characters.

        Only show characters that ``_viewable_characters`` returns.

        """
        characters = _viewable_characters(request.user)
        character_table_cls = tables.character_table(request.user)
        table = character_table_cls(characters)
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
        if character not in _viewable_characters(request.user):
            return http.HttpResponseForbidden(
                'Error: you do not have the rights to view this character.'
            )
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
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Attempt to save changes. Reply.
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
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )
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
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

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
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )
        return render(
            request,
            'gurps_manager/character_templates/character-id-delete-form.html',
            {'character': character}
        )

class CharacterIdSkills(View):
    """Handle a request for ``character/<id>/skills``."""
    def get(self, request, character_id):
        """Return information about character ``character_id``'s skills."""
        # Check whether the character exists, and whether the user owns it.
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Reply.
        table = tables.CharacterSkillTable(
            models.CharacterSkill.objects.filter(character=character_id)
        )
        RequestConfig(request).configure(table)
        return render(
            request,
            'gurps_manager/character_templates/character-id-skills.html',
            {'character': character, 'table': table, 'request': request}
        )

    def post(self, request, character_id):
        """Create and update a character's skills"""
        # Check whether the character exists, and whether the user owns it.
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Attempt to save changes. Reply.
        formset_cls = forms.character_skill_formset(character)
        formset = formset_cls(request.POST, instance=character)
        if formset.is_valid():
            formset.save()
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-character-id-skills',
                args=[character_id]
            ))
        else:
            # Put formset data into session. Destination view will use it.
            request.session['form_data'] = json.dumps(formset.data)
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-character-id-skills-update-form',
                args=[character_id]
            ))

class CharacterIdSkillsUpdateForm(View):
    """Handle a request for ``character/<id>/skills/update-form``."""
    def get(self, request, character_id):
        """Return a form for updating character ``character_id``'s skills."""
        # Check whether the character exists, and whether we own it.
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Generate a form.
        formset_cls = forms.character_skill_formset(character)
        form_data = request.session.pop('form_data', None)
        if form_data is None:
            formset = formset_cls(instance=character)
        else:
            formset = formset_cls(json.loads(form_data))

        # Reply.
        return render(
            request,
            'gurps_manager/character_templates/character-id-skills-update-form.html', # pylint: disable=C0301
            {'character': character, 'formset': formset}
        )

class CharacterIdSpells(View):
    """Handle a request for ``character/<id>/spells``."""
    def get(self, request, character_id):
        """Return information about character ``character_id``'s spells."""
        # Check whether the character exists, and whether the user owns it.
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Reply.
        table = tables.CharacterSpellTable(
            models.CharacterSpell.objects.filter(character=character_id)
        )
        RequestConfig(request).configure(table)
        return render(
            request,
            'gurps_manager/character_templates/character-id-spells.html',
            {'character': character, 'table': table, 'request': request}
        )

    def post(self, request, character_id):
        """Create and update a character's spells"""
        # Check whether the character exists, and whether the user owns it.
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Attempt to save changes. Reply.
        formset_cls = forms.character_spell_formset(character)
        formset = formset_cls(request.POST, instance=character)
        if formset.is_valid():
            formset.save()
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-character-id-spells',
                args=[character_id]
            ))
        else:
            # Put formset data into session. Destination view will use it.
            request.session['form_data'] = json.dumps(formset.data)
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-character-id-spells-update-form',
                args=[character_id]
            ))

class CharacterIdSpellsUpdateForm(View):
    """Handle a request for ``character/<id>/spells/update-form``."""
    def get(self, request, character_id):
        """Return a form for updating character ``character_id``'s spells."""
        # Check whether the character exists, and whether the user owns it.
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Generate a form.
        formset_cls = forms.character_spell_formset(character)
        form_data = request.session.pop('form_data', None)
        if form_data is None:
            formset = formset_cls(instance=character)
        else:
            formset = formset_cls(json.loads(form_data))

        # Reply.
        return render(
            request,
            'gurps_manager/character_templates/character-id-spells-update-form.html', # pylint: disable=C0301
            {'character': character, 'formset': formset}
        )

class CharacterIdPossessions(View):
    """Handle a request for ``character/<id>/possessions``."""
    def get(self, request, character_id):
        """Return information about character ``character_id``'s possessions."""
        # Check whether the character exists, and whether the user owns it.
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Generate a reply.
        table = tables.PossessionTable(
            models.Possession.objects.filter(character=character_id)
        )
        RequestConfig(request).configure(table)
        return render(
            request,
            'gurps_manager/character_templates/character-id-possessions.html',
            {'character': character, 'table': table, 'request': request}
        )

    def post(self, request, character_id):
        """Create and update a character's possessions"""
        # Check whether the character exists, and whether the user owns it.
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Attempt to save changes. Reply.
        formset_cls = forms.possession_formset(character)
        formset = formset_cls(request.POST, instance=character)
        if formset.is_valid():
            formset.save()
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-character-id-possessions',
                args=[character_id]
            ))
        else:
            # Put formset data into session. Destination view will use it.
            request.session['form_data'] = json.dumps(formset.data)
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-character-id-possessions-update-form',
                args=[character_id]
            ))

class CharacterIdPossessionsUpdateForm(View):
    """Handle a request for ``character/<id>/possessions/update-form``."""
    def get(self, request, character_id):
        """Return a form for updating character ``character_id``'s possessions.""" # pylint: disable=C0301
        # Check whether the character exists, and whether the user owns it.
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Generate a form.
        formset_cls = forms.possession_formset(character)
        form_data = request.session.pop('form_data', None)
        if form_data is None:
            formset = formset_cls(instance=character)
        else:
            formset = formset_cls(json.loads(form_data))

        # Reply.
        return render(
            request,
            'gurps_manager/character_templates/character-id-possessions-update-form.html', # pylint: disable=C0301
            {'character': character, 'formset': formset}
        )

class CharacterIdTraits(View):
    """Handle a request for ``character/<id>/traits/``."""
    def get(self, request, character_id):
        """Return information about character ``character_id``'s traits."""
        # Check whether the character exists, and whether the user owns it.
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Generate a reply.
        table = tables.TraitTable(
            models.Trait.objects.filter(character=character_id)
        )
        RequestConfig(request).configure(table)
        return render(
            request,
            'gurps_manager/character_templates/character-id-traits.html',
            {'character': character, 'table': table, 'request': request}
        )

    def post(self, request, character_id):
        """Create and update a character's traits"""
        # Check whether the character exists, and whether the user owns it.
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Attempt to save changes. Reply.
        formset_cls = forms.trait_formset()
        formset = formset_cls(request.POST, instance=character)
        if formset.is_valid():
            formset.save()
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-character-id-traits',
                args=[character_id]
            ))
        else:
            # Put formset data into session. Destination view will use it.
            request.session['form_data'] = json.dumps(formset.data)
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-character-id-traits-update-form',
                args=[character_id]
            ))

class CharacterIdTraitsUpdateForm(View):
    """Handle a request for ``character/<id>/traits/update-form``."""
    def get(self, request, character_id):
        """Return a form for updating character ``character_id``'s traits.""" # pylint: disable=C0301
        # Check whether the character exists, and whether the user owns it.
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Generate a form.
        formset_cls = forms.trait_formset()
        form_data = request.session.pop('form_data', None)
        if form_data is None:
            formset = formset_cls(instance=character)
        else:
            formset = formset_cls(json.loads(form_data))

        # Reply.
        return render(
            request,
            'gurps_manager/character_templates/character-id-traits-update-form.html', # pylint: disable=C0301
            {'character': character, 'formset': formset}
        )

class CharacterIdHitLocations(View):
    """Handle a request for ``character/<id>/hit-locations``."""
    def get(self, request, character_id):
        """Return information about character ``character_id``'s hit-locations.""" # pylint: disable=C0301
        # Check whether the character exists, and whether the user owns it.
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Generate a reply.
        table = tables.HitLocationTable(
            models.HitLocation.objects.filter(character=character_id)
        )
        RequestConfig(request).configure(table)
        return render(
            request,
            'gurps_manager/character_templates/character-id-hit-locations.html',
            {'character': character, 'table': table, 'request': request}
        )

    def post(self, request, character_id):
        """Create and update a character's hit-locations"""
        # Check whether the character exists, and whether the user owns it.
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Attempt to save changes. Reply.
        formset_cls = forms.hit_location_formset()
        formset = formset_cls(request.POST, instance=character)
        if formset.is_valid():
            formset.save()
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-character-id-hit-locations',
                args=[character_id]
            ))
        else:
            # Put formset data into session. Destination view will use it.
            request.session['form_data'] = json.dumps(formset.data)
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-character-id-hit-locations-update-form',
                args=[character_id]
            ))

class CharacterIdHitLocationsUpdateForm(View):
    """Handle a request for ``character/<id>/hit-locations/update-form``."""
    def get(self, request, character_id):
        """Return a form for updating character ``character_id``'s hit-locations.""" # pylint: disable=C0301
        # Check whether the character exists, and whether the user owns it.
        character = _get_model_object_or_404(models.Character, character_id)
        if not _user_owns_character(request.user, character):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Generate a form.
        formset_cls = forms.hit_location_formset()
        form_data = request.session.pop('form_data', None)
        if form_data is None:
            formset = formset_cls(instance=character)
        else:
            formset = formset_cls(json.loads(form_data))

        # Reply.
        return render(
            request,
            'gurps_manager/character_templates/character-id-hit-locations-update-form.html', # pylint: disable=C0301
            {'character': character, 'formset': formset}
        )

class CampaignIdItems(View):
    """Handle a request for ``campaign/<id>/items``."""
    def get(self, request, campaign_id):
        """Return information about campaign ``campaign_id``'s items.""" # pylint: disable=C0301
        # Check whether the campaign exists, and whether the user owns it.
        campaign = _get_model_object_or_404(models.Campaign, campaign_id)
        if not _user_owns_campaign(request.user, campaign):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Generate a reply.
        table = tables.ItemTable(
            models.Item.objects.filter(campaign=campaign_id)
        )
        RequestConfig(request).configure(table)
        return render(
            request,
            'gurps_manager/campaign_templates/campaign-id-items.html',
            {'campaign': campaign, 'table': table, 'request': request}
        )

    def post(self, request, campaign_id):
        """Create and update a campaign's items"""
        # Check whether the campaign exists, and whether the user owns it.
        campaign = _get_model_object_or_404(models.Campaign, campaign_id)
        if not _user_owns_campaign(request.user, campaign):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Attempt to save changes. Reply.
        formset_cls = forms.campaign_items_formset()
        formset = formset_cls(request.POST, instance=campaign)
        if formset.is_valid():
            formset.save()
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-campaign-id-items',
                args=[campaign_id]
            ))
        else:
            # Put formset data into session. Destination view will use it.
            request.session['form_data'] = json.dumps(formset.data)
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-campaign-id-items-update-form',
                args=[campaign_id]
            ))

class CampaignIdItemsUpdateForm(View):
    """Handle a request for ``campaign/<id>/items/update-form``."""
    def get(self, request, campaign_id):
        """Return a form for updating campaign ``campaign_id``'s items.""" # pylint: disable=C0301
        # Check whether the campaign exists, and whether the user owns it.
        campaign = _get_model_object_or_404(models.Campaign, campaign_id)
        if not _user_owns_campaign(request.user, campaign):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Generate a form.
        formset_cls = forms.campaign_items_formset()
        form_data = request.session.pop('form_data', None)
        if form_data is None:
            formset = formset_cls(instance=campaign)
        else:
            formset = formset_cls(json.loads(form_data))

        # Reply.
        return render(
            request,
            'gurps_manager/campaign_templates/campaign-id-items-update-form.html', # pylint: disable=C0301
            {'campaign': campaign, 'formset': formset}
        )

class CampaignIdSpells(View):
    """Handle a request for ``campaign/<id>/spells``."""
    def get(self, request, campaign_id):
        """Return information about campaign ``campaign_id``'s spells.""" # pylint: disable=C0301
        # Check whether the campaign exists, and whether the user owns it.
        campaign = _get_model_object_or_404(models.Campaign, campaign_id)
        if not _user_owns_campaign(request.user, campaign):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Generate a reply.
        table = tables.SpellTable(
            models.Spell.objects.filter(campaign=campaign_id)
        )
        RequestConfig(request).configure(table)
        return render(
            request,
            'gurps_manager/campaign_templates/campaign-id-spells.html',
            {'campaign': campaign, 'table': table, 'request': request}
        )

    def post(self, request, campaign_id):
        """Create and update a campaign's spells"""
        # Check whether the campaign exists, and whether the user owns it.
        campaign = _get_model_object_or_404(models.Campaign, campaign_id)
        if not _user_owns_campaign(request.user, campaign):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Attempt to save changes. Reply.
        formset_cls = forms.campaign_spells_formset()
        formset = formset_cls(request.POST, instance=campaign)
        if formset.is_valid():
            formset.save()
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-campaign-id-spells',
                args=[campaign_id]
            ))
        else:
            # Put formset data into session. Destination view will use it.
            request.session['form_data'] = json.dumps(formset.data)
            return http.HttpResponseRedirect(reverse(
                'gurps-manager-campaign-id-spells-update-form',
                args=[campaign_id]
            ))

class CampaignIdSpellsUpdateForm(View):
    """Handle a request for ``campaign/<id>/spells/update-form``."""
    def get(self, request, campaign_id):
        """Return a form for updating campaign ``campaign_id``'s spells.""" # pylint: disable=C0301
        # Check whether the campaign exists, and whether the user owns it.
        campaign = _get_model_object_or_404(models.Campaign, campaign_id)
        if not _user_owns_campaign(request.user, campaign):
            return http.HttpResponseForbidden(
                'Error: you do not own this character.'
            )

        # Generate a form.
        formset_cls = forms.campaign_spells_formset()
        form_data = request.session.pop('form_data', None)
        if form_data is None:
            formset = formset_cls(instance=campaign)
        else:
            formset = formset_cls(json.loads(form_data))

        # Reply.
        return render(
            request,
            'gurps_manager/campaign_templates/campaign-id-spells-update-form.html', # pylint: disable=C0301
            {'campaign': campaign, 'formset': formset}
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
    >>> other_user.is_superuser = True
    >>> _user_owns_character(other_user, character)
    True

    """
    if character.owner == user or character.campaign.owner == user:
        return True
    elif user.is_superuser:
        return True
    return False

def _user_owns_campaign(user, campaign):
    """Check whether ``user`` owns ``campaign``, directly or indirectly.

    Return ``True`` if ``user`` owns ``campaign``, or if ``user`` owns the
    campaign to which ``campaign`` belongs. Else, return ``False``.

    >>> from gurps_manager import factories
    >>> campaign = factories.CampaignFactory.create()
    >>> _user_owns_campaign(campaign.owner, campaign)
    True
    >>> other_user = factories.UserFactory.create()
    >>> _user_owns_campaign(other_user, campaign)
    False
    >>> other_user.is_superuser = True
    >>> _user_owns_campaign(other_user, campaign)
    True

    """
    if campaign.owner == user:
        return True
    elif user.is_superuser:
        return True
    return False

def _viewable_characters(user):
    """Return a list of characters that ``user`` can view.

    ``user`` is a ``User`` model object. That is, ``user`` is a user of the
    application.

    Only return characters that fulfill one of the following conditions:
    * the user owns that character
    * the user is the game master for that character's campaign
    * the user is an Admin

    Additionally, include other characters in the same campaigns as the
    characters above.

    >>> from gurps_manager import factories
    >>> campaign = factories.CampaignFactory.create()
    >>> character1 = factories.CharacterFactory.create(campaign=campaign)
    >>> character2 = factories.CharacterFactory.create(campaign=campaign)
    >>> characters = _viewable_characters(campaign.owner)
    >>> len(characters)
    2
    >>> character1 in characters
    True
    >>> character2 in characters
    True
    >>> characters = _viewable_characters(character1.owner)
    >>> len(characters)
    2
    >>> character1 in characters
    True
    >>> character2 in characters
    True
    >>> characters = _viewable_characters(character2.owner)
    >>> len(characters)
    2
    >>> character1 in characters
    True
    >>> character2 in characters
    True

    """
    # The user owns these characters directly, or the user is the game master
    # for these characters.
    characters = models.Character.objects.filter(
        Q(owner__exact=user) |
        Q(campaign__owner__exact=user)
    )

    # find all campaigns that the above characters belong to
    campaigns = set()
    for character in characters:
        campaigns.add(character.campaign)

    # finally, find all "related" characters
    return models.Character.objects.filter(campaign__in=campaigns)

def _viewable_campaigns(user):
    """Return a list of campaigns that ``user`` can view.

    ``user`` is a ``User`` model object. That is, ``user`` is a user of the
    application.

    Only return campaigns that fulfill one of the following conditions:
    * the user owns that character
    * the user is the game master for that character's campaign
    * the user is an Admin

    Additionally, include other campaigns in the same campaigns as the
    campaigns above.

    >>> from gurps_manager import factories
    >>> user = factories.UserFactory.create()
    >>> other_user = factories.UserFactory.create()
    >>> campaign = factories.CampaignFactory.create(owner=user)
    >>> campaigns = _viewable_campaigns(user)
    >>> campaign in campaigns
    True
    >>> campaigns = _viewable_campaigns(other_user)
    >>> campaign in campaigns
    False
    >>> other_user.is_superuser = True
    >>> campaigns = _viewable_campaigns(other_user)
    >>> campaign in campaigns
    True

    """

    characters = models.Character.objects.filter(owner=user)
    participating_campaigns = set()
    for character in characters:
        participating_campaigns.add(character.campaign)

    owned_campaigns = set()
    for campaign in models.Campaign.objects.filter(owner__exact=user):
        owned_campaigns.add(campaign)

    if user.is_superuser:
        return models.Campaign.objects.all()
    else:
        return participating_campaigns.union(owned_campaigns)
