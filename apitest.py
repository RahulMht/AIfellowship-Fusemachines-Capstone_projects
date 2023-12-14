import tweepy
import pandas as pd
import streamlit as st
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pickle

# Load the saved tokenizer
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the saved MAX_SEQUENCE_LENGTH
with open('max_sequence_length.txt', 'r') as f:
    MAX_SEQUENCE_LENGTH = int(f.read())

# Load the saved model
model = load_model('Sentiment_CNN_model.h5')

# Define the tokenizer function
def tokenize_text(text):
    # Tokenize text
    x_test = pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=MAX_SEQUENCE_LENGTH)
    return x_test

def get_tweet_sentiment(text):
    # Tokenize and preprocess the tweet
    processed_tweet = tokenize_text(text)
    # Predict sentiment using the loaded model
    prediction = model.predict(processed_tweet)
    
    # Classify sentiment based on prediction
    if prediction >= 0.7:
        return 'positive'
    elif 0.3 < prediction < 0.7:
        return 'neutral'
    else:
        return 'negative'

consumer_key = 'XXAzixSAcBlGZijKaZ8sITqcW'
consumer_secret = 'KiwGzslBFLKaBqMOfXFpXgZ96FkBIqxQMYmjaXU0bdYENr8ffJ'
access_token = '1328476524-KLO2rMfdF16UZdgsZ3Co0LxT4V3FYbHhOnE0Ma6'
access_token_secret = 'aFpNeXCo2Of5kCDAkA52514DRJ6TMJ6X9H5Cr3UNHvOOe'

# Pass in our twitter API authentication key
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret,
    access_token, access_token_secret
)

# Instantiate the tweepy API
api = tweepy.API(auth, wait_on_rate_limit=True)

# Streamlit app
st.title('Twitter Sentiment Analysis')

# Input field for search query
search_query = st.text_input("Enter search query:", "'ref''world cup'-filter:retweets AND -filter:replies AND -filter:links")
no_of_tweets = 10

if st.button("Search"):
    try:
        # The number of tweets we want to retrieve from the search
        tweets = api.search_tweets(q=search_query, lang="en", count=no_of_tweets, tweet_mode ='extended')
        
        # Pulling Some attributes from the tweet
        attributes_container = [[tweet.user.name, tweet.created_at, tweet.favorite_count, tweet.source, tweet.full_text] for tweet in tweets]

        # Creation of column list to rename the columns in the dataframe
        columns = ["User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet"]
        
        # Creation of DataFrame
        tweets_df = pd.DataFrame(attributes_container, columns=columns)

        # Perform sentiment analysis on tweets_df
        st.write("Sample Tweets:")
        for idx, tweet_text in enumerate(tweets_df['Tweet'].values[:10]):
            sentiment = get_tweet_sentiment(tweet_text)
            st.write(f"Tweet {idx + 1}: {tweet_text}")
            st.write(f"Sentiment: {sentiment}")
            st.write("-------------")

    except BaseException as e:
        st.error(f"Status Failed On: {str(e)}")
