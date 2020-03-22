<template>
  <header class ="header"> <nuxt-link to="/"><img alt="logo" src="@/assets/logo.png" /></nuxt-link> </header>
</template>

<style lang="scss">
  .header {
    width: 100%;
    background-color: white;
    margin: 0 auto;
    display: block;
    padding: 40px 0;
    a {
      display: block;
      width: 200px;
      margin: auto;
      img {
        margin: auto;
      }
    }
  }

</style>
