<template>
  <v-container fill-height>
    <v-layout justify-center align-center color="blue lighten-2">
      <v-row>
        <v-form ref="form" v-model="valid" class="form">
          <v-container>
            <h1 class="blue--text headline">
              In welchem PLZ-Gebiet leben Sie?
            </h1>
            <br />
            <v-text-field
              v-model="area"
              required
              solo
              :rules="[v => !!v.match(zipRegexp) || 'Bitte geben Sie PLZ ein.']"
              label="z.B. 10115" />
          </v-container>

          <div class="float-right text-right">
            <v-btn
              outlined
              color="primary"
              class="mr-4"
              @click.stop="previousQuestion">Zurück</v-btn>
            <v-btn
              color="primary"
              class="mr-4"
              @click.stop="nextQuestion">Weiter</v-btn>
          </div>
        </v-form>
      </v-row>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      valid: false,
      error: false,
      errorMessage: null,
      zipRegexp: /^(?!01000)(?!99999)(0[1-9]\d{3}|[1-9]\d{4})$/
    }
  },
  head() {
    return {
      meta: [{
        hid: 'description',
        name: 'description',
      }]
    }
  },
  computed: {
    area: {
      get() {
        return this.$store.state.area
      },
      set(response) {
        this.$store.commit('updateArea', response)
      },
    }
  },
  methods: {
    previousQuestion() {
      this.$router.push({
        name: 'index'
      })
    },
    nextQuestion() {
      this.$refs.form.validate()
      if (this.area.match(this.zipRegexp)) {
        this.$router.push({
          name: 'submit'
        })
      }
    }
  }
}
</script>
