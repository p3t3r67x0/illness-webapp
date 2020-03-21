<template>
<div class="min-h-screen flex items-center justify-center bg-green-400">
  <div class="container p-3">
    <h1 class="text-2xl text-white mb-3">
      Welche Symptome haben Sie?
    </h1>
    <form v-on:submit.prevent="nextQuestion">
      <small v-if="error" class="inline-block bg-red-600 text-white p-3">{{ errorMessage }}</small>
      <input type="text" class="w-full text-xl p-2 mb-3" v-model="response" placeholder="Husten, Schüttelfrost">
      <div class="text-right">
        <button class="cursor-pointer inline-block bg-gray-100 hover:bg-gray-400 py-2 px-6">Weiter</button>
      </div>
    </form>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      error: false,
      errorMessage: null
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
  watch: {
    response: function() {
      if (this.response.length > 2) {
        this.error = false
      }
    }
  },
  methods: {
    nextQuestion() {
      if (this.response.length > 2) {
        this.$router.push({
          name: 'area'
        })
      } else {
        this.error = true
        this.errorMessage = 'Bitte geben Sie mindestens ein Symptome an'
      }
    }
  }
}
</script>
