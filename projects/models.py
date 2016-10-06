from django.db import models

class Project(models.Model):
    initials = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True)
    analytic_code = models.CharField(max_length=20, blank=True)
    parent_project = models.ForeignKey('self', default=None, blank=True,
            null=True, related_name='childs', on_delete=models.SET_DEFAULT)
    is_closed = models.BooleanField(default=False)

    class Meta:
        index_together = ["parent_project", "initials"]
        unique_together = ["parent_project", "initials"]

    def get_full_initials(self):
        i = self.initials.upper()
        if self.parent_project:
            i = self.parent_project.get_full_initials() +':'+ i
        return i



    def __str__(self):
        t = '{} - {}'.format(self.get_full_initials(), self.description)

        if self.childs.count():
            t += ' ({})'.format(self.childs.count())

        return t
