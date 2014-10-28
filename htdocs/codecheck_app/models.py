from django.db import models
from sitemonitor.models import File
from django.conf import settings

# Create your models here.
class FileReview(models.Model):
    file = models.ForeignKey(File)
    note = models.TextField(null=True, blank=True)
    last_reviewed_date = models.DateTimeField(null=True, blank=True)
    last_reviewed_user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def __unicode__(self):
        return self.note
