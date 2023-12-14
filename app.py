import streamlit as st
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from streamlit_lottie import st_lottie 
import json
import requests
import pickle
import os

col1, col2 = st.columns([1, 1])

with col1:

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

    # Streamlit app
    st.title('Twitter Sentiment Analysis')

    user_input = st.text_input("Enter a tweet for sentiment analysis")

    if st.button('Submit'):
        processed_input = tokenize_text(user_input)
        prediction = model.predict(processed_input)
        if prediction >= 0.7:
            st.success(f"Positive sentiment 😊")
            st.slider('Sentiment Score', 0,10, int (prediction*10))
        elif 0.3 < prediction < 0.7:  # Adjusted the condition to check for values between 0.4 and 0.7
            st.info(f"Neutral sentiment 🙂")
            st.slider('Sentiment Score', 0,10, int(prediction*10))
        else:
            st.warning(f"Negative sentiment 😖")
            st.slider('Sentiment Score', 0,10, int(prediction*10))
with col2:
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    lottie_hello = load_lottieurl("https://lottie.host/22856a7c-7ef0-453d-81ea-dc5842ab763a/p0C048YfUz.json")
    
    st_lottie(
        lottie_hello,
        speed=1,
        reverse=False,
        loop=True,
        quality="high", 
        width=300,
        height=300,
        key=None,
    )

