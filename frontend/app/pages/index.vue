<template>
<div class="flex items-center justify-center">
  <div class="container p-3">
    <h1 class="text-2xl text-white mb-3">
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
                    class="mb-3"></multiselect>
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
    this.$axios.$get('https://illness.403.io/api/v1/symptom/?format=json').then(res => {
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
