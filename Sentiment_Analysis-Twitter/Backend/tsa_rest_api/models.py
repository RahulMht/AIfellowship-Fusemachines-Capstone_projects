from django.db import models


# Create your models here.
class ClassifiedTweets(models.Model):
    tweet = models.CharField(max_length=350)
    sentiment = models.CharField(max_length=20)


class TrainedData(models.Model):
    logprior = models.TextField()
    loglikelihood = models.TextField()
