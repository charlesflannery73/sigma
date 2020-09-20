import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver


logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    logger.info('user={user}, action=login, data=[{ip}]'.format(user=user,ip=ip))


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    logger.info('user={user}, action=logout, data=[{ip}]'.format(user=user,ip=ip))


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    logger.info('user={user}, action=login_fail, data=[{ip}]'.format(user=credentials['username'], ip=ip))
