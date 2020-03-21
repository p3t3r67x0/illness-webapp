<template>
<div class="min-h-screen flex justify-center bg-green-400 md:py-12">
  <div class="container p-3">
    <h1 class="text-2xl text-white mb-3">
      Übersicht der eingereichten Daten.
    </h1>
    <div v-for="result, index in results.result" :key="index">
      <div v-if="result.symptoms != '' && result.symptoms != null" class="bg-gray-200 p-3 mt-3">
        <h3 class="font-bold">Symptome</h3>
        <p class="mb-3">{{ result.symptoms }}</p>
        <h3 class="font-bold">PLZ Gebiet</h3>
        <p>{{ result.area }}</p>
      </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      results: []
    }
  },
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
    this.$axios.$get('http://localhost:5000/illness').then(res => {
      console.log(res)
      this.results = res
    }).catch((error) => {
      console.log(error)
    })
  }
}
</script>
