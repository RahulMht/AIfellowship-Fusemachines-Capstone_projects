from rest_framework import serializers
from tsa_rest_api.models import ClassifiedTweets, TrainedData


class ClassifiedTweetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassifiedTweets
        fields = ('tweet', 'sentiment')


class TrainedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainedData
        fields = ('logprior', 'loglikelihood')
