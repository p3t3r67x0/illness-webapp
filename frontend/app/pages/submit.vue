<template>
<div class="min-h-screen flex items-center justify-center bg-green-400">
  <div class="p-3">
    <h1 class="text-2xl text-white mb-3">
      Geschafft! Ihre Daten werden übermittelt.
    </h1>
    <div class="text-center">
      <a v-on:click.stop="previousQuestion" class="cursor-pointer inline-block bg-gray-100 hover:bg-gray-400 py-2 px-6">Zurück</a>
    </div>
  </div>
</div>
</template>

<script>
export default {
  head() {
    return {
      title: 'tbd.',
      meta: [{
        hid: 'description',
        name: 'description',
        content: 'tbd.'
      }]
    }
  },
  created() {
    this.$axios.$post(process.env.API_URL + '/illness', {
      area: this.$store.state.area,
      symptoms: this.$store.state.symptoms
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
