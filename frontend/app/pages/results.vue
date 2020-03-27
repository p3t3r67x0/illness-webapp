<template>
<div class="flex justify-center md:py-12">
  <div class="container p-3">
    <h1 class="text-2xl mb-3 text-blue-600">
      Übersicht der eingereichten Daten
    </h1>
    <h3 class="text-xl">Filter</h3>
    <input type="text" class="sm:w-1/4 border border-blue-600 rounded text-xl p-2 mb-3" v-model="county" placeholder="Landkreis">
    <input type="text" class="sm:w-1/4 border border-blue-600 rounded text-xl p-2 mb-3" v-model="zipCode" placeholder="PLZ">
    <client-only>
      <date-picker v-model="date" format="DD-MM-YYYY" valueType="YYYY-MM-DD" :disabled-date="notAfterToday" class="sm:w-1/4 border border-blue-600 rounded text-xl mb-3" placeholder="DD-MM-YYYY"></date-picker>
    </client-only>
    <div id="map"></div>
    <ul class="list text-blue-600">
      <li v-for="(item, index) in results" :key="index">
        <div class="rounded overflow-hidden shadow-lg">
          <div class="px-6 py-4">
            <strong class="text-base">
              {{ item.county }}
            </strong>
          </div>
          <div class="px-6 py-4">
            <span v-for="symptom in formatSymptoms(item.symptoms)" class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2">{{ symptom }}</span>
          </div>
        </div>
      </li>
    </ul>
    <div class="scroll-to-top">
      <a class="cursor-pointer rounded inline-block bg-blue-600 hover:bg-blue-800 text-white py-2 px-6" v-on:click.stop="scrollToTop">&#8593;</a>
    </div>
  </div>
</div>
</template>

<script>
import { groupBy } from '../utils';
import { stringify as queryStringify } from 'query-string';

export default {
  data() {
    return {
      results: [],
      date: null,
      county: null,
      today: new Date(),
      zipCode: null,
      zipCodeRegex: /^(?!01000|99999)(0[1-9]\d{3}|[1-9]\d{4})$/,
      heatMapLayer: null,
      heatMapConfig: {
        // radius should be small ONLY if scaleRadius is true (or small radius is intended)
        // if scaleRadius is false it will be the constant radius used in pixels
        "radius": 20,
        "maxOpacity": .8,
        // scales the radius based on map zoom
        "scaleRadius": false,
        // if set to false the heatmap uses the global maximum for colorization
        // if activated: uses the data maximum within the current map boundaries
        //   (there will always be a red spot with useLocalExtremas true)
        "useLocalExtrema": true,
        // which field name in your data represents the latitude - default "lat"
        latField: 'lat',
        // which field name in your data represents the longitude - default "lng"
        lngField: 'lng',
        // which field name in your data represents the data value - default "value"
        valueField: 'count'
      },
      heatMapStructure: {
        max: 2,
        data: []
      }
    }
  },
  async created() {
    try {
      await this.getResult()
      const HeatmapOverlay = await require ('@/assets/leaflet-heatmap.js')
      this.heatMapLayer = new HeatmapOverlay(this.heatMapConfig)

      new L.Map('map', {
        dragging: !L.Browser.mobile,
        maxZoom: 10,
        tap: !L.Browser.mobile,
        center: new L.LatLng(51.37328923, 10.21334121),
        zoom: 6,
        layers: [new L.TileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}{r}.png'), this.heatMapLayer]
      })

      this.updateMap()
    } catch (e) {
      console.log(e)
    }
  },
  watch: {
    zipCode: async function() {
      if (this.zipCodeRegex.test(this.zipCode) || this.zipCode === '') {
        this.getFilterResult()
      }
    },
    county: async function() {
      if (this.county.length > 0 || this.county === '') {
        this.getFilterResult()
      }
    },
    date: async function() {
      this.getFilterResult()
    }
  },
  methods: {
    notAfterToday(date) {
      return date > this.today
    },
    async getFilterResult() {
      const queryParams = {}

      if (this.date) {
        queryParams.date = this.date
      }
      if(this.county) {
        queryParams.county = this.county
      }
      if(this.zipCodeRegex.test(this.zipCode)) {
        queryParams.zip_code = this.zipCode
      }

      const query = queryStringify(queryParams)

      try {
        const results = await this.$axios.$get(`${process.env.API_URL}/report/result/?${query}`)
        this.results = this.normalizeResponse(results)
        this.updateMap()
      } catch (e) {
        console.log(e)
      }
    },
    async getResult() {
      try {
        const results = await this.$axios.$get(`${process.env.API_URL}/report/result/`)
        this.results = this.normalizeResponse(results)
      } catch (e) {
        console.log(e)
      }
    },
    normalizeResponse(response) {
      const groupedResponse = groupBy(response, 'county')
      return Object.keys(groupedResponse)
        .map(county => {
          return {
            county,
            longitude: groupedResponse[county][0].longitude,
            latitude: groupedResponse[county][0].latitude,
            symptoms: groupedResponse[county].map((item) => {
              return { [item.symptom]: item.users_count_affected }
            }).reduce((a, b) => Object.assign(a, b), {})
          }
        });
    },
    formatSymptoms(symptoms) {
      return Object.keys(symptoms).map((symptom, index) => {
        return `${symptom}: ${Object.values(symptoms)[index]}`
      })
    },
    scrollToTop() {
      window.scrollTo({
        top: 0,
        left: 0,
        behavior: 'smooth'
      });
    },
    updateMap() {
      this.heatMapStructure.data = []
      this.results.forEach((item) => {
          this.heatMapStructure.data.push({
            lat: Number(item.latitude),
            lng: Number(item.longitude)
          })
      })

      this.heatMapLayer.setData(this.heatMapStructure)
    }
  }
}
</script>

<style lang="scss">
  #map {
    position: relative;
    display: block;
    height: 600px;
  }

  .list {
    padding: 20px 0;
  }

  .scroll-to-top {
    width: 100%;
    margin: 0;
    text-align: right;
    position: fixed;
    display: block;
    bottom: 16px;
    right: 16px;
    > a {
      opacity: .5;
      left: -16px;
    }
  }
</style>
