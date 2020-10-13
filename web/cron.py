import kronos
from .models import Signature
from datetime import date
from django.utils import timezone

@kronos.register('1 0 * * *')
def expire_sigs():
    Signature.objects.filter(expiry__lte=date.today(), status__exact='enabled').update(status='expired', modified=timezone.now())
