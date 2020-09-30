import kronos
from .models import Signature
from datetime import date, datetime


@kronos.register('* * * * *')
def expire_sigs():
    Signature.objects.filter(expiry__lte=date.today(), status__exact='enabled').update(status='expired', modified=datetime.now())
