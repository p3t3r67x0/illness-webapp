<template>
<div class="layout min-h-full min-h-screen bg-green-400">
  <header-component />
  <nuxt />
</div>
</template>

<script>
  import HeaderComponent from '../components/Header.vue'
  export default {
    components: {
      HeaderComponent
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
