# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Resolution(models.Model):
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text
