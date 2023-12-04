<template>
  <v-container fluid>
    <v-row no-gutters>
      <v-col cols="12">
        <v-text-field v-model="query.search" rounded filled append-icon="fa-solid fa-magnifying-glass" autofocus
                      placeholder="Search for keywords..." @click:append="searchTweets()" @change="searchTweets()"
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row v-if="tweets.length>0" no-gutters>
      <v-col cols="3">
        <v-card
          class="mt-4 mx-auto"
          max-width="250"
        >
          <v-sheet
            class="title v-sheet--offset mx-auto d-flex justify-content-center"
            color="transparent"
          >
            <h1 class="pa-2">{{ positive_tweet_count }}</h1>
          </v-sheet>

          <v-card-text class="pt-0">
            <div class="title font-weight-light mb-2">
              Positive Tweet Count
            </div>
            <div class="subheading font-weight-light grey--text">
              Total number of positive tweets
            </div>
          </v-card-text>
        </v-card>
        <v-card
          class="mt-4 mx-auto"
          max-width="250"
        >
          <v-sheet
            class="title v-sheet--offset mx-auto d-flex justify-content-center"
            color="transparent"
          >
            <h1 class="pa-2">{{ negative_tweet_count }}</h1>
          </v-sheet>

          <v-card-text class="pt-0">
            <div class="title font-weight-light mb-2">
              Negative Tweet Count
            </div>
            <div class="subheading font-weight-light grey--text">
              Total number of negative tweets
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="9">
        <highchart :options="chartOptions"/>
      </v-col>

    </v-row>
    <v-row v-if="tweets.length>0">
      <v-col cols="12">
        <v-data-table
          calculate-widths
          :class="this.$vuetify.theme.dark  ?'table-dark':'table-light'"
          :headers="headers"
          :items="tweets"
          :loading="tweetIsLoading"
          :items-per-page="10"

        >
          <template v-slot:item.processed_tweet="{ item }">
            <template
              v-for="chip in item.processed_tweet"
            >
              {{ chip }}
            </template>
          </template>
          <template v-slot:item.likelihood="{ item }">
            {{ item.likelihood.toFixed(2) }}
          </template>
          <template v-slot:item.sentiment="{ item }">
            <v-chip :color="item.likelihood>0?'#4CAF50':'#F44336'" dark>
              {{ item.sentiment }}
            </v-chip>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: 'DashboardPage',
  data() {
    return {
      headers: [
        {text: "Tweet", value: "text"},
        {text: "Preprocessed Tweet", value: "processed_tweet"},
        {text: "Likelihood", value: "likelihood"},
        {text: "Sentiment", value: "sentiment"},

      ],
      query: {
        search: "",
      },
      chartOptions: {
        chart: {
          plotBackgroundColor: null,
          plotBorderWidth: null,
          plotShadow: false,
          type: 'pie'
        },
        title: {
          text: "Positive Tweets v/s Negative Tweets"
        },
        accessibility: {
          point: {
            valueSuffix: '%'
          }
        },
        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
              enabled: true,
              format: '<b>{point.name}</b>: {point.percentage:.1f} %'
            }
          }
        },
        series: [
          {
            name: 'No. of Tweets',
            colorByPoint: true,
            data: [
              {
                name: "Positive Tweets",
                y: 50
              },
              {
                name: "Negative Tweets",
                y: 50
              }
            ]
          }
        ]
      }
    }
  },
  computed: {
    ...mapGetters("apis", [
      "tweets", "tweetIsLoading", "positive_tweet_count", "negative_tweet_count"
    ]),
  },
  watch: {
    positive_tweet_count() {
      this.redraw()
    },
    negative_tweet_count() {
      this.redraw()
    },
  },
  methods: {
    ...mapActions("apis", [
      "fetchTweets"
    ]),
    searchTweets() {
      this.fetchTweets(this.query).then(function (res) {
        console.log(res)
      })
    },
    redraw() {
      this.chartOptions.series[0].data[0].y=this.positive_tweet_count;
      this.chartOptions.series[0].data[1].y=this.negative_tweet_count;
    }

  }
}
</script>

<style scoped lang="scss">
.table-light {
  background-color: #F5F5F5;
  border-radius: 30px;
  padding: 16px;
}

.table-dark {
  background-color: #272727;
  border-radius: 30px;
  padding: 16px;
}
</style>
