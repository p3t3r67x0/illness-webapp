<template>
<div class="flex justify-center py-32">
  <div class="container p-3">
    <h1 class="text-2xl text-blue-600 mb-3">
      In welchem PLZ-Gebiet leben Sie?
    </h1>
    <form v-on:submit.prevent="nextQuestion">
      <small v-if="error" class="inline-block bg-red-600 text-white p-3">{{ errorMessage }}</small>
      <input type="text" class="w-full border border-blue-600 rounded text-xl p-2 mb-3" v-model="response" placeholder="10115" pattern="^(?!01000)(?!99999)(0[1-9]\d{3}|[1-9]\d{4})$">
      <div class="text-right">
        <a v-on:click.stop="previousQuestion" class="cursor-pointer rounded inline-block bg-blue-600 hover:bg-blue-800 text-white py-2 px-6 mr-2">Zurück</a>
        <a v-on:click="nextQuestion" class="cursor-pointer rounded inline-block bg-blue-600 hover:bg-blue-800 text-white py-2 px-6">Weiter</a>
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
    response: {
      get() {
        return this.$store.state.area
      },
      set(response) {
        this.$store.commit('updateArea', response)
      },
    }
  },
  watch: {
    response: function() {
      if (this.response.match(this.zipRegexp)) {
        this.error = false
      }
    }
  },
  methods: {
    previousQuestion() {
      this.$router.push({
        name: 'index'
      })
    },
    nextQuestion() {
      if (this.response.match(this.zipRegexp)) {
        this.$router.push({
          name: 'submit'
        })
      } else {
        this.error = true
        this.errorMessage = 'Bitte geben Sie PLZ ein.'
      }
    }
  }
}
</script>
