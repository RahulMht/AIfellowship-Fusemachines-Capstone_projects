const state = () => ({
  tweets: [],
  positive_tweet_count: 0,
  negative_tweet_count: 0,
  tweetIsLoading: false,
  classifierIsTraining: false,
  trainingResult: {
    loglikelihood:[]
  }
});

const mutations = {
  setTweets: (state, tweets) => {
    state.tweets = tweets

  },
  setTrainingResult: (state, trainingResult) => {
   state.trainingResult=trainingResult
    // state.trainingResult = Object.entries(trainingResult.loglikelihood).map(([key, value]) => ({role:key, ...value}))
    // state.trainingResult = [{"word":k,"score":v} for k,v in trainingResult.loglikelihood.items()]
  },
  setPositiveTweetCount: (state, positive_tweet_count) => {
    state.positive_tweet_count = positive_tweet_count
  },
  setNegativeTweetCount: (state, negative_tweet_count) => {
    state.negative_tweet_count = negative_tweet_count

  }, setTweetIsLoading: (state, tweetIsLoading) => {
    state.tweetIsLoading = tweetIsLoading
  }, setClassifierIsTraining: (state, classifierIsTraining) => {
    state.classifierIsTraining = classifierIsTraining
  }
};

const actions = {
  async startTraining(state) {
    state.commit('setClassifierIsTraining', true);
    let url = `${process.env.START_TRAINING_CLASSIFIER_API}`;

    await this.$axios.get(url, {
      headers: {
        Accept: "application/json",
      }
    })
      .then(res => {
        state.commit('setTrainingResult', res.data.data)
        state.commit('setClassifierIsTraining', false);
      }).catch(err => {
        console.log('error', err);
        state.commit('setClassifierIsTraining', false);
      });
  },

  async fetchTweets(state, query = null) {
    let search = '';
    if (query !== null) {
      search = query.search;
    }
    state.commit('setTweetIsLoading', true);
    let url = `${process.env.FETCH_TWEETS_API}`;

    url = `${url}?search=${search}`


    await this.$axios.get(url, {
      headers: {
        Accept: "application/json",
      }
    })
      .then(res => {
        const tweets = res.data.data.tweets;
        const positive_tweet_count = res.data.data.positive_tweet_count;
        const negative_tweet_count = res.data.data.negative_tweet_count;
        state.commit('setTweets', tweets);
        state.commit('setPositiveTweetCount', positive_tweet_count);
        state.commit('setNegativeTweetCount', negative_tweet_count);
        state.commit('setTweetIsLoading', false);
      }).catch(err => {
        console.log('error', err);
        state.commit('setTweetIsLoading', false);
      });
  },
};

const getters = {
  tweets: state => state.tweets,
  trainingResult: state => state.trainingResult,
  positive_tweet_count: state => state.positive_tweet_count,
  negative_tweet_count: state => state.negative_tweet_count,
  tweetIsLoading: state => state.tweetIsLoading,
  classifierIsTraining: state => state.classifierIsTraining,
};

export default {
  state, mutations, actions, getters,
};

