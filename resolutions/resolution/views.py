# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from .models import Resolution

import random

class ResolutionView(TemplateView):

    def get(self, request, **kwargs):

        """ Show all resolutions received
        """

        template = 'resolutions.html'
        context = {}

        show_logo_instead = random.randint(0, 100)
        if show_logo_instead <= 15:
            # 15% of the time, show the logo instead
            context['show_logo_instead'] = True
        else:
            resolution_id = request.session.get('next_resolution')
            if resolution_id:
                try:
                    resolution = Resolution.objects.get(id=resolution_id)
                except Exception:
                    resolution = False
            else:
                # If we don't have a "next resolution," start at the beginning
                try:
                    resolution = Resolution.objects.first()
                except Exception:
                    resolution = False

            if resolution:
                resolutions_count = Resolution.objects.count()
                context['resolutions_count'] = resolutions_count
                context['resolution'] = resolution
                context['resolution_id'] = resolution.id
                try:
                    request.session['next_resolution'] = resolution.get_next_by_created_at().id
                except Exception:
                    # If there isn't a "next", loop back to the beginning
                    request.session['next_resolution'] = Resolution.objects.first().id
            else:
                # This should never happen as long as there is at least one Resolution loaded in.
                # But just to be safe and avoid error screens, show the logo.
                context['resolution_id'] = False
                context['show_logo_instead'] = True

        return render(request, template, context)

    def post(self, request, **kwargs):

        """ Used by the Twilio API to receive a text message and save a resolution.
        """

        resolution = request.POST.get('Body')

        if resolution:
            new_resolution = Resolution(text=resolution)
            new_resolution.save()

        template = 'response.html'
        context = {}
        return render(request, template, context)
