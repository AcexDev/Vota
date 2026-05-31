from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Poll(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
class Question(models.Model):
    POLL_TYPES = [
        ('MCQ', 'Multiple Choice'),
        ('TEXT', 'Opend-Ended')
    ]
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.TextField()
    type = models.CharField(max_length=10, choices=POLL_TYPES)
    
class Options(models.Model):                                         #Only for MCQ
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    image = models.ImageField(null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    vote_count = models.IntegerField(default=0)


class Answer(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)  
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Options, on_delete=models.CASCADE, 
                                        null=True, blank=True)
    text_answer = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'poll', 'question')

