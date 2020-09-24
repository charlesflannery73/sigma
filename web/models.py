from django.db import models
import datetime
import timedelta
from django.utils import timezone


class Type(models.Model):

    name = models.CharField(max_length=255, null=False, unique=True)
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Signature(models.Model):

    ENABLED = 'enabled'
    DISABLED = 'disabled'
    TESTING = 'testing'
    PENDING = 'pending'
    EXPIRED = 'expired'
    STATUS = [
        (ENABLED, 'enabled'),
        (DISABLED, 'disabled'),
        (TESTING, 'testing'),
        (PENDING, 'pending'),
        (EXPIRED, 'expired'),
    ]
    text = models.TextField(null=False, unique=True)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    reference = models.CharField(max_length=255, null=False)
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    expiry = models.DateField(null=False, default=datetime.date.today() + timezone.timedelta(91))
    status = models.CharField(max_length=255, choices=STATUS, default=ENABLED)


    def __str__(self):
        return self.text
