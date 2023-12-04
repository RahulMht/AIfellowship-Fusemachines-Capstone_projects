import nltk
import numpy as np
from nltk.corpus import stopwords, twitter_samples

import re

import json


def get_all_positive_tweets():
    """
    Get all positive tweets from training data json file
    :return:
    """
    all_positive_tweets = twitter_samples.strings('positive_tweets.json')
    return all_positive_tweets


def get_english_stop_words():
    """
    Get all english stop words from training data
    :return:
    """
    english_stop_words = stopwords.words('english')
    return english_stop_words


def get_all_negative_tweets():
    """
    Get all negative tweets from training data json file
    :return:
    """
    all_negative_tweets = twitter_samples.strings('negative_tweets.json')
    return all_negative_tweets


def remove_hyperlinks_marks_styles(tweet):
    """
    Remove hyperlinks, Twitter marks and styles

    :param tweet:
    :return:
    """
    # remove old style retweet text "RT"
    new_tweet = re.sub(r'^RT[\s]+', '', tweet)

    # remove hyperlinks
    new_tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', new_tweet)

    # remove hashtags
    # only removing the hash # sign from the word
    new_tweet = re.sub(r'#', '', new_tweet)

    return new_tweet


def tokenize_tweet(tweet, tokenizer):
    """
    Tokenize the string i.e. split the string into individual words.

    :param tweet:
    :return:
    """

    tweet_tokens = tokenizer.tokenize(tweet)

    return tweet_tokens


def remove_stopwords_punctuations(tweet_tokens, stopwords_english, punctuations):
    """
    Remove stop words and punctuations that doesn't add significant meaning to the text.

    :param tweet_tokens:
    :return:
    """

    tweets_clean = []
    for word in tweet_tokens:
        if word not in stopwords_english and word not in punctuations:
            tweets_clean.append(word)

    return tweets_clean


def get_stem(tweets_clean, stemmer):
    """
    Stemming the word into its most general form. E.g: learning, learned, learnt -> learn

    :param tweets_clean:
    :return:
    """
    tweets_stem = []

    for word in tweets_clean:
        stem_word = stemmer.stem(word)
        tweets_stem.append(stem_word)

    return tweets_stem


def process_tweet(tweet, tokenizer, stopwords_english, punctuations, stemmer):
    """
    Combine all the preprocessing techniques.

    :param tokenizer:
    :param tweet:
    :return:
    """
    processed_tweet = remove_hyperlinks_marks_styles(tweet)
    tweet_tokens = tokenize_tweet(processed_tweet, tokenizer)
    tweets_clean = remove_stopwords_punctuations(tweet_tokens, stopwords_english, punctuations)
    tweets_stem = get_stem(tweets_clean, stemmer)

    return tweets_stem


def create_frequency(tweets, ys, tokenizer, stopwords_english, punctuations, stemmer):
    freq_d = {}

    for tweet, y in zip(tweets, ys):
        for word in process_tweet(tweet, tokenizer, stopwords_english, punctuations, stemmer):
            pair = (word, y)

            if pair in freq_d:
                freq_d[pair] += 1

            else:
                freq_d[pair] = freq_d.get(pair, 1)
    return freq_d


def train_naive_bayes_model(tokenizer, stopwords_english, punctuations, freqs, train_y):
    loglikelihood = {}
    logprior = 0

    # calculate the number of unique words in vocab
    unique_words = set([pair[0] for pair in freqs.keys()])
    V = len(unique_words)

    # calculate N_pos and N_neg
    N_pos = N_neg = 0
    for pair in freqs.keys():
        if pair[1] > 0:
            N_pos += freqs[(pair)]
        else:
            N_neg += freqs[(pair)]

    # Calculate the number of documents (tweets)
    D = train_y.shape[0]

    # Calculate D_pos, the number of positive documents (tweets)
    D_pos = sum(train_y)

    # Calculate D_neg, the number of negative documents (tweets)
    D_neg = D - D_pos

    # Calculate logprior
    logprior = np.log(D_pos) - np.log(D_neg)

    # for each unqiue word
    for word in unique_words:
        # get the positive and negative frequency of the word
        freq_pos = freqs.get((word, 1), 0)
        freq_neg = freqs.get((word, 0), 0)

        # calculate the probability that word is positive, and negative
        p_w_pos = (freq_pos + 1) / (N_pos + V)
        p_w_neg = (freq_neg + 1) / (N_neg + V)

        # calculate the log likelihood of the word
        loglikelihood[word] = np.log(p_w_pos / p_w_neg)

    return logprior, loglikelihood


def naive_bayes_predict(tweet, logprior, loglikelihood, tokenizer, stopwords_english, punctuations, stemmer):
    # Process the tweet to get a list of words
    word_l = process_tweet(tweet, tokenizer, stopwords_english, punctuations, stemmer)

    # Initialize probability to zero
    p = 0

    # Add the logprior
    p += logprior

    for word in word_l:

        # Get log likelihood of each keyword
        if word in loglikelihood:
            p += loglikelihood[word]
    return p,word_l
