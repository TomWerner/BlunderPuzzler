import datetime

from django.db import models

severities = (
    ('1', 'Inaccuracy'),
    ('2', 'Mistake'),
    ('4', 'Blunder')
)


class Puzzle(models.Model):
    link = models.CharField(max_length=50)
    severity = models.CharField(max_length=1, choices=severities)

    def iframe_link(self):
        return '//' + self.link.replace('http://', '')

    def severity_class(self):
        return self.get_severity_display().lower()