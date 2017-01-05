import datetime

from django.db import models
from django.db.models import Avg

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

    def get_rating(self):
        if self.puzzlerating_set.count() < 2:
            return 3
        result = round(self.puzzlerating_set.all().aggregate(Avg('rating'))['rating__avg'], 2)
        print(result)
        return result

    def add_rating(self, rating):
        if not (1 <= int(rating) <= 5):
            raise RuntimeError("Invalid rating")
        else:
            PuzzleRating(puzzle=self, rating=rating).save()


class PuzzleRating(models.Model):
    puzzle = models.ForeignKey(Puzzle)
    rating = models.IntegerField()