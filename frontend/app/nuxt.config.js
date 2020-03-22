
export default {
  mode: 'universal',
  /*
  ** Headers of the page
  */
  server: {
    port: 3000, // default: 3000
    host: '0.0.0.0' // default: localhost
  },
  head: {
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  env: {
    API_URL: process.env.API_URL || 'https://covi.403.io/api/v1'
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: 'orange' },
  /*
  ** Global CSS
  */
  css: [
    '~/node_modules/leaflet/dist/leaflet.css'
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    // Doc: https://github.com/nuxt-community/nuxt-tailwindcss
    '@nuxtjs/tailwindcss',
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/dotenv',
    'nuxt-vue-multiselect',
    'nuxt-leaflet'
  ],
  purgeCSS: {
     whitelistPatterns: [
       /multiselect/
     ]
   },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend (config, ctx) {
    },
    vendor: ['@johmun/vue-tags-input']
  }
}
