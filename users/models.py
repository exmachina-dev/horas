from django.db import models
from django.conf import settings

# Create your models here.
class Employee(models.Model):
    initials = models.CharField(primary_key=True, max_length=5)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        help_text="User binded to this employee", related_name='user_account')
    color = models.CharField(
        max_length=25, default="#af0000",
        help_text="Color in CSS format (hexadecimal or rgb format)")
    is_active = models.BooleanField(default=True,
        help_text="Wether the employee is active in the company or not.")
    production_ratio = models.FloatField(null=True)

    class Meta:
        ordering = ('initials',)

    def __str__(self):
        return '{} - {}'.format(self.initials, self.user.first_name)
