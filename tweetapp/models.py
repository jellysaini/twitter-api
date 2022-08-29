from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator
