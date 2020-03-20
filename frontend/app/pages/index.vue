<template>
<div class="min-h-screen flex items-center justify-center bg-green-400">
  <div class="p-3">
    <h1 class="text-2xl text-white mb-3">
      Welche Symptome haben Sie?
    </h1>
    <form class="mb-3">
      <input type="text" class="w-full text-xl p-2" v-model="response" placeholder="Husten, Schüttelfrost">
    </form>
    <div class="text-right">
      <button v-on:click="postResponse" class="bg-gray-100 p-2">Weiter</button>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      response: null,
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
  asyncData(context) {
    context.$axios.$get('https://jsonplaceholder.typicode.com/todos/1').then(res => {
      console.log(res)
    }).catch((error) => {
      console.log(error)
    })
  },
  methods: {
    postResponse(query) {
      this.$axios.$post('https://jsonplaceholder.typicode.com/posts', {
        topic: this.response
      }).then(res => {
        console.log(res)
      }).catch((error) => {
        console.log(error)
      })
    }
  }
}
</script>
