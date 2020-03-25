<template>
  <v-container fill-height>
        <v-layout justify-center align-center color="blue lighten-2">
            <v-form ref="form" v-model="valid" class="form">
                <h1 class="blue--text headline">
                  Welche Symptome haben Sie?
                </h1>
                <br />
                <v-select
                  v-model="response"
                  :items="results"
                  item-text="name"
                  item-value="id"
                  required
                  chips
                  label="z.B. Husten, Schüttelfrost"
                  multiple
                  solo
                  :rules="[v => v.length !== 0 || 'Bitte geben Sie mindestens ein Symptom an']"
                ></v-select>
                <div class="float-right text-right">
                  <v-btn
                    color="primary"
                    class="mr-4"
                    @click="nextQuestion">Weiter</v-btn>
                  <br /><br />
                  <v-btn
                    outlined
                    color="primary"
                    class="mr-4"
                    @click.stop="$router.push({
                             name: 'results'
                           })">Zur Symptomkarte</v-btn>
                </div>
            </v-form>
        </v-layout>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      valid: false,
      results: [],
      data: null
    }
  },
  head() {
    return {
      meta: [{
        hid: 'description',
      }]
    }
  },
  created() {
    this.$axios.$get(`${process.env.API_URL}/symptom/?format=json`).then(res => {
      this.results = res
    }).catch((error) => {
      console.log(error)
    })
  },
  computed: {
    response: {
      get() {
        return this.$store.state.symptoms
      },
      set(response) {
        this.$store.commit('updateSymptoms', response)
      },
    }
  },
  methods: {
    nextQuestion () {
      this.$refs.form.validate()
      if (this.valid) {
        this.$router.push({
          name: 'area'
        })
      }
    }
  }
}
</script>

<style lang="scss">
  .form {
    width: 100%;
  }
</style>
