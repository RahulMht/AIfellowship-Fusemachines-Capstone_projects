<template>
  <v-container>
    <v-row>
      <h1>Naive Bayes Classifier Training</h1>
      <v-spacer></v-spacer>
      <v-btn :loading="classifierIsTraining" color="primary" depressed @click="startTraining()">
        <v-icon left>fa-solid fa-circle-play</v-icon>
        Start Training
      </v-btn>
    </v-row>
    <v-row>
      <p>You can train the Naive Bayes Classifier used for sentiment analysis in this project by clicking on the start
        training button. The train results will be shown when the training is completed. The training dataset used is
        NLTK data corpus twitter samples containing 5000 positive tweets and 5000 negative tweets.</p>
    </v-row>

    <v-row v-if="trainingResult.loglikelihood.length > 0">
      <v-col cols="12">
        <v-data-table
          calculate-widths
          :class="this.$vuetify.theme.dark  ?'table-dark':'table-light'"
          :headers="headers"
          :items="trainingResult.loglikelihood"
          :loading="classifierIsTraining"
          :items-per-page="10"

        >
        </v-data-table>
      </v-col>
    </v-row>

  </v-container>
</template>

<script>
import {mapActions, mapGetters} from "vuex";

export default {
  name: 'TrainClassifierPage',
  data() {
    return {
      headers: [
        {text: "Word", value: "word"},
        {text: "Likelihood", value: "likelihood"},
      ],
    }
  },
  computed: {
    ...mapGetters("apis", [
      "classifierIsTraining","trainingResult",
    ])
  },
  methods: {
    ...mapActions("apis", [
      "startTraining"
    ]),
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
