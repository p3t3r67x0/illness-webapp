<template>
<div class="min-h-screen flex justify-center bg-blue-400 py-12">
  <div class="container">
    <h1 class="text-5xl text-white mb-3">
      Fragenkatalog
    </h1>
    <div class="bg-gray-400 p-3">
      <form class="" v-on:submit.prevent="postResponse">
        <div>
          <p class="mb-2">Fragentyp</p>
          <select v-model="responseType" class="w-full text-xl p-2 mb-3">
            <option value="text">Textfrage</option>
            <option value="select">Auswahlfrage</option>
            <option value="checkbox">Checkboxfrage</option>
          </select>
        </div>
        <div>
          <p class="mb-2">Frage</p>
          <input type="text" class="w-full text-xl p-2 mb-3" v-model="response">
        </div>
        <div v-if="responseType == 'text'">
          <p class="mb-2">Platzhaltertext</p>
          <input type="text" class="w-full text-xl p-2 mb-3" v-model="placeholder">
        </div>
        <div v-if="responseType == 'select'">
          <p class="mb-2">Auswahlfrage</p>
          <div v-for="option in options" :key="option.id">
            <input v-model="option.value" class="w-1/2 text-xl p-2 mb-3">
          </div>
          <div class="w-1/2 text-right">
            <a @click="addInput" class="cursor-pointer bg-gray-100 p-2">Add input</a>
          </div>
        </div>
        <div v-if="responseType == 'checkbox'">
          <p class="mb-2">Checkboxfrage</p>
          <div v-for="option in options" :key="option.id">
            <input v-model="option.value" class="w-1/2 text-xl p-2 mb-3">
          </div>
          <div class="w-1/2 text-right">
            <a @click="addInput" class="cursor-pointer bg-gray-100 p-2">Add input</a>
          </div>
        </div>
        <div class="text-right">
          <button class="cursor-pointer bg-gray-100 p-2">Speichern</button>
        </div>
      </form>
    </div>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      response: null,
      placeholder: null,
      responseType: 'text',
      optionsCounter: 0,
      options: [{
        id: 'option0',
        value: null
      }],
      checkboxsCounter: 0,
      checkboxs: [{
        id: 'checkbox0',
        value: null
      }],
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
    },
    addInput() {
      this.options.push({
        id: `option${++this.optionsCounter}`,
        value: null
      });
    }
  }
}
</script>
