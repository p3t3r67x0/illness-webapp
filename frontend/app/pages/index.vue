<template>
<div class="flex justify-center py-32">
  <div class="container p-3">
    <h1 class="text-2xl text-blue-600 mb-3">
      Welche Symptome haben Sie?
    </h1>
    <form v-on:submit.prevent="nextQuestion">
      <small v-if="error" class="inline-block bg-red-600 text-white p-3">{{ errorMessage }}</small>
      <multiselect  v-model="response"
                    tag-placeholder="Add this as new tag"
                    placeholder="Husten, Schüttelfrost"
                    label="name"
                    track-by="id"
                    :options="results"
                    :multiple="true"
                    :taggable="true"
                    @tag="addTag"
                    class="w-full border border-blue-600 rounded text-xl mb-3"></multiselect>
      <div class="text-right">
        <button class="cursor-pointer rounded inline-block bg-blue-600 hover:bg-blue-800 text-white py-2 px-6">Weiter</button>
      </div>
    </form>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      results: [],
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
  created() {
    this.$axios.$get(`${process.env.API_URL}/symptom/?format=json`).then(res => {
      console.log(res.results)
      this.results = res.results
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
      if (this.response.length > 0) {
        this.error = false
      }
    }
  },
  methods: {
    addTag (newTag) {
      const tag = {
        name: newTag,
        id: newTag.substring(0, 2) + Math.floor((Math.random() * 10000000))
      }
      this.response = [...this.response, tag]
      this.$store.commit('updateSymptoms', [...this.$store.state.symptoms, tag])
    },
    nextQuestion() {
      if (this.response.length > 0) {
        this.$router.push({
          name: 'area'
        })
      } else {
        this.error = true
        this.errorMessage = 'Bitte geben Sie mindestens ein Symptom an'
      }
    }
  }
}
</script>
