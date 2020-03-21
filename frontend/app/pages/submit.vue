<template>
<div class="min-h-screen flex items-center justify-center bg-green-400">
  <div class="p-3">
    <h1 class="text-2xl text-white mb-3">
      Ihre Antwort wird übermittelt!
    </h1>
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
    this.$axios.$post('http://localhost:5000/illness', {
      area: this.$store.state.area,
      symptoms: this.$store.state.symptoms
    }).then(res => {
      console.log(res)
    }).catch((error) => {
      console.log(error)
    })
  }
}
</script>
