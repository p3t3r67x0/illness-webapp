<template>
  <v-container fill-height>
    <v-layout justify-center align-center color="blue lighten-2">
      <v-container class="container">
        <v-row>
          <h1 class="blue--text headline">
            Geschafft! Ihre Daten werden übermittelt
          </h1>
          </v-row>
        <br />
          <v-row align="center">
          <v-btn
            outlined
            color="primary"
            @click.stop="previousQuestion">Zurück</v-btn>
            </v-row>
        <br />
        oder
        <br />
        <br />
        <v-row>
          <v-btn
            color="primary"
            @click.stop="$router.push({
                               name: 'results'
                             })">
            Zur Symptomkarte
          </v-btn>
        </v-row>
      </v-container>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  head() {
    return {
      meta: [{
        hid: 'description',
      }]
    }
  },
  created() {
    const { symptoms } = this.$store.state

    try {
      this.$axios.$post(`${process.env.API_URL}/report/`, {
        zip_code: this.$store.state.area,
        symptoms: symptoms.map(i => i.id)
      })
    } catch (e) {
      console.log(e)
    }
  },
  methods: {
    previousQuestion() {
      this.$router.push({
        name: 'area'
      })
    }
  }
}
</script>

<style lang="scss">
  .container {
    align-items: center;
    justify-content: center;
    display: flex;
    flex-direction: column;
  }
</style>
