<template>
<div class="min-h-screen flex items-center justify-center bg-green-400">
  <div class="container p-3">
    <h1 class="text-2xl text-white mb-3">
      In welchem PLZ Gebiet leben Sie?
    </h1>
    <form v-on:submit.prevent="nextQuestion">
      <input type="text" class="w-full text-xl p-2 mb-3" v-model="response" placeholder="732">
      <div class="text-right">
        <a v-on:click.stop="previousQuestion" class="cursor-pointer inline-block bg-gray-100 hover:bg-gray-400 py-2 px-6 mr-2">Zurück</a>
        <a v-on:click="nextQuestion" class="cursor-pointer inline-block bg-gray-100 hover:bg-gray-400 py-2 px-6">Weiter</a>
      </div>
    </form>
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
  asyncData(context) {
    context.$axios.$get('https://jsonplaceholder.typicode.com/todos/1').then(res => {
      console.log(res)
    }).catch((error) => {
      console.log(error)
    })
  },
  computed: {
    response: {
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
      this.$router.push({
        name: 'submit'
      })
    }
  }
}
</script>
