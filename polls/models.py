import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

# Each model has a number of class variables,
# each of which represents a database field in the model.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self): # add representative name
        return self.question_text
    
    @admin.display( #properties configurable via the decorator,
        boolean=True,
        ordering="pub_date",
        description="Published recently?"
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


    def __str__(self): # add representative name
        return self.choice_text
