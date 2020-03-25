<template>
  <v-app>
    <header-component />
    <v-content class="content">
      <nuxt />
    </v-content>
    <footer-component />
  </v-app>
</template>

<script>
import HeaderComponent from '../components/header.vue'
import FooterComponent from '../components/footer.vue'

export default {
  components: {
    HeaderComponent,
    FooterComponent
  },
  head() {
    return {
      title: 'covi'
    }
  }
}
</script>

<style lang="scss">
  .content {
    max-width: 1200px;
    margin: auto;
    width: 100%;
  }
</style>
