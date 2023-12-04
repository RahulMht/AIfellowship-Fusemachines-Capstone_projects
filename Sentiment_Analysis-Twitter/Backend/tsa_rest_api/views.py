import numpy as np
import tweepy
import string
import json

from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tsa_backend_project import settings
from tsa_rest_api.models import ClassifiedTweets, TrainedData
from tsa_rest_api.serializers import ClassifiedTweetsSerializer, TrainedDataSerializer
from tsa_backend_project.helpers import get_english_stop_words, get_all_positive_tweets, get_all_negative_tweets, \
    create_frequency, train_naive_bayes_model, naive_bayes_predict
from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer


@csrf_exempt
def index(request, id=0):
    # Show individual data or specific data.
    if request.method == 'GET':
        try:
            id
        except NameError:
            classified_tweets = ClassifiedTweets.objects.all()
            classified_tweets_serializer = ClassifiedTweetsSerializer(classified_tweets, many=True)
            return JsonResponse(classified_tweets_serializer.data, safe=False)
        else:
            classified_tweets = ClassifiedTweets.objects.get(id=id)
            classified_tweets_serializer = ClassifiedTweetsSerializer(classified_tweets, many=False)
            return JsonResponse(classified_tweets_serializer.data, safe=False)

    # Add new data.
    elif request.method == 'POST':
        classified_tweets_data = JSONParser().parse(request)
        classified_tweets_serializer = ClassifiedTweetsSerializer(data=classified_tweets_data)
        if classified_tweets_serializer.is_valid():
            classified_tweets_serializer.save()
            return JsonResponse("Data added successfully", safe=False)
        return JsonResponse("Failed to add new data", safe=False)

    # Update existing data.
    elif request.method == 'PUT':
        classified_tweets_data = JSONParser().parse(request)
        classified_tweet = ClassifiedTweets.objects.get(id=id)
        classified_tweets_serializer = ClassifiedTweetsSerializer(classified_tweet, data=classified_tweets_data)
        if classified_tweets_serializer.is_valid():
            classified_tweets_serializer.save()
            return JsonResponse("Data updated successfully", safe=False)
        return JsonResponse("Failed to update data", safe=False)

    # Delete existing data.
    elif request.method == 'DELETE':
        classified_tweet = ClassifiedTweets.objects.get(id=id)
        classified_tweet.delete()
        return JsonResponse("Data deleted successfully", safe=False)


@csrf_exempt
def train_classifier(request):
    # Initialize necessary classes
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                               reduce_len=True)

    punctuations = string.punctuation
    stopwords_english = get_english_stop_words()
    stemmer = PorterStemmer()

    # Split training and test data
    all_positive_tweets = get_all_positive_tweets()
    all_negative_tweets = get_all_negative_tweets()

    test_pos = all_positive_tweets[4000:]
    train_pos = all_positive_tweets[:4000]
    test_neg = all_negative_tweets[4000:]
    train_neg = all_negative_tweets[:4000]

    train_x = train_pos + train_neg
    test_x = test_pos + test_neg

    train_y = np.append(np.ones(len(train_pos)), np.zeros(len(train_neg)))
    test_y = np.append(np.ones(len(test_pos)), np.zeros(len(test_neg)))

    # build the frequency dictionary
    freqs = create_frequency(train_x, train_y, tokenizer, stopwords_english, punctuations, stemmer)

    logprior, loglikelihood = train_naive_bayes_model(tokenizer, stopwords_english, punctuations, freqs, train_y)

    trained_data = TrainedData.objects.first()
    if trained_data is not None:
        trained_data.delete()

    trained_data_serializer = TrainedDataSerializer(data={
        "logprior": logprior,
        "loglikelihood": json.dumps(loglikelihood),
    })

    if trained_data_serializer.is_valid():
        trained_data_serializer.save()

    converted_loglikelihood = []
    for k, v in loglikelihood.items():
        converted_loglikelihood.append({'word': k, 'likelihood': v})

    return JsonResponse(
        {"message": "Classifier trained successfully",
         "data": {
             "logprior": logprior,
             "loglikelihood": converted_loglikelihood,
             "no_of_positive_tweets": len(all_positive_tweets),
             "no_of_negative_tweets": len(all_negative_tweets),
         }},
        status=200,
        safe=False)


@csrf_exempt
def classify_tweets(request):
    if request.GET.get('search', None) == "":
        return JsonResponse({"message": "Cannot fetch tweets for empty search"},
                            status=400,
                            safe=False)

    # Add parameters to search query for discarding retweets and only take tweets in english language
    search = request.GET.get('search', None) + " -is:retweet" + " lang:en"
    if request.method == 'GET':
        tweepy_client = tweepy.Client(bearer_token=settings.TWITTER_BEARER_TOKEN)
        recent_tweets = (
            tweepy_client.search_recent_tweets(query=search, max_results=100, expansions=['author_id'],
                                               tweet_fields=['created_at', 'lang']))

        # Initialize necessary classes
        tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                                   reduce_len=True)
        punctuations = string.punctuation
        stopwords_english = get_english_stop_words()
        stemmer = PorterStemmer()

        trained_data = TrainedData.objects.first()

        if trained_data is not None:
            logprior = float(trained_data.logprior)
            loglikelihood = json.loads(trained_data.loglikelihood)
        else:
            return JsonResponse(
                {"message": "The naive bayes classifier has not been trained yet. Please train the classifier first"},
                status=400,
                safe=False)

        tweets = []
        positive_count = 0
        negative_count = 0
        for tweet in recent_tweets.data:
            p, processed_tweet = naive_bayes_predict(tweet.data['text'], logprior, loglikelihood, tokenizer,
                                                     stopwords_english,
                                                     punctuations,
                                                     stemmer)
            tweet.data['likelihood'] = p
            tweet.data['sentiment'] = 'Positive' if p > 0 else 'Negative'
            positive_count = positive_count + 1 if p > 0 else positive_count
            negative_count = negative_count if p > 0 else negative_count + 1
            tweet.data['processed_tweet'] = processed_tweet
            tweets.append(tweet.data)

        return JsonResponse(
            {"message": "Tweets successfully fetched.",
             "data": {"tweets": tweets, "positive_tweet_count": positive_count,
                      "negative_tweet_count": negative_count}},
            status=200,
            safe=False)
