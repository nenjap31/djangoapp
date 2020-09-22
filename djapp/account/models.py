from django.db import models
from django.contrib.auth.models import User
from partner.models import Partner
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Account(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=30,null=True, blank=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        import inspect
        for frame_record in inspect.stack():
            if frame_record[3] == 'get_response':
                request = frame_record[0].f_locals['request']
                break
        else:
            request = None
        if request:
            if request.user.is_superuser:
                partner = None
            else:
                entry = Account.objects.get(user_id=request.user.id)
                partner = Partner.objects.get(id=entry.partner_id)

            if not request.user.is_superuser:
                Account.objects.create(user=instance, partner=partner)


@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    else:
        request = None
    if request:
        if not request.user.is_superuser:
            instance.account.save()