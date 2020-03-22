<template>
<div class="layout min-h-full min-h-screen">
  <header-component />
  <nuxt />
  <footer-component />
</div>
</template>

<script>
import HeaderComponent from '../components/header.vue'
import FooterComponent from '../components/footer.vue'

export default {
  components: {
    HeaderComponent,
    FooterComponent
  }
}
</script>

<style lang="scss">
  .layout {
    display: flex;
    flex-direction: column;
    > div {
      flex: auto;
    }
  }
</style>
