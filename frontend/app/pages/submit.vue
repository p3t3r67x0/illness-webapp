<template>
<div class="flex justify-center py-32">
  <div class="container p-3">
    <h1 class="text-center text-2xl text-blue-600 mb-3">
      Geschafft! Ihre Daten werden übermittelt
    </h1>
    <div class="text-center">
      <a v-on:click.stop="previousQuestion" class="cursor-pointer rounded inline-block bg-blue-600 hover:bg-blue-800 text-white py-2 px-6">Zurück</a>
      <div class="text-blue-600">- oder -</div>
      <a class="cursor-pointer rounded inline-block bg-blue-600 hover:bg-blue-800 text-white py-2 px-6" v-on:click.stop="$router.push({
        name: 'results'
      })">Zur Übersicht der eingereichten Daten.</a>
    </div>
  </div>
</div>
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
    const symptoms = this.$store.state.symptoms
    let symptomsId = []

    for (let symptom of symptoms) {
      symptomsId.push(symptom.id)
    }

    console.log(symptomsId)
    this.$axios.$post(`${process.env.API_URL}/report/`, {
      zip_code: this.$store.state.area,
      symptoms: symptomsId
    }).then(res => {
      console.log(res)
    }).catch((error) => {
      console.log(error)
    })
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
