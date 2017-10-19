# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
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
            resolution_id = kwargs.get('id')

            if resolution_id:
                most_recent_id = request.session.get('most_recent_id')
                try:
                    resolution_id = int(resolution_id)
                    most_recent_id = int(most_recent_id)
                except Exception:
                    pass

                if resolution_id == most_recent_id:
                    # We just saw this one, so increment the resolution ID by one to get the next.
                    resolution_id = resolution_id + 1
                try:
                    resolution = Resolution.objects.get(id=resolution_id)
                    resolutions_count = Resolution.objects.count()
                    context['resolutions_count'] = resolutions_count
                    context['resolution'] = resolution
                    context['resolution_id'] = resolution.id
                    request.session['most_recent_id'] = resolution.id
                    return render(request, template, context)
                except Exception:
                    resolution = False
            else:
                resolution = False
            
            if not resolution:
                # If no id is specified, get the first.
                # This will also have the side effect of looping back to the beginning.
                # Though if there are any gaps / non-contiguous spaces in the numbering, it will send you to the beginning too.
                # If I had more time to fuss with this, I would make that not so.
                try:
                    resolution = Resolution.objects.first()
                except Exception:
                    resolution = False

            if resolution:
                return HttpResponseRedirect('/{0}'.format(resolution.id))
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
