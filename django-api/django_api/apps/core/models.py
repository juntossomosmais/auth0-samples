from django.db import models


class StandardModelMixin(models.Model):
    id = models.AutoField(primary_key=True, editable=False, verbose_name="Id")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated at")

    class Meta:
        abstract = True


class AuditAction(StandardModelMixin):
    user_id = models.CharField(max_length=128, null=False, blank=False)
    action = models.CharField(max_length=128, null=False, blank=False)
    success = models.BooleanField(null=False, blank=False)
    # Later we can identify where the anonymous user is using the following:
    # https://docs.djangoproject.com/en/3.2/ref/contrib/gis/geoip2/
    ip_address = models.GenericIPAddressField(null=True)

    def __str__(self):
        return f"{self.user_id} / {self.action} / {self.ip_address} / {self.created_at.date()}"
