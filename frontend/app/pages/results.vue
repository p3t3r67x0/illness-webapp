<template>
<div class="flex justify-center md:py-12">
  <div class="container p-3">
    <h1 class="text-2xl mb-3 text-blue-600">
      Übersicht der eingereichten Daten
    </h1>
    <form class="block mb-3">
      <input type="text" class="w-1/4 border border-blue-600 rounded text-xl p-2 mb-3" v-model="zipCode" placeholder="10115">
    </form>
    <div id="map"></div>
    <ul class="list text-blue-600">
      <li v-for="(item, index) in normalizeResponse(results)" :key="index">
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

export default {
  data() {
    return {
      map: null,
      results: [],
      zipCode: null,
      zipCodeRegex: /^(?!01000|99999)(0[1-9]\d{3}|[1-9]\d{4})$/,
      heatmapOverlay: null,
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
      const results = await this.$axios.$get(`${process.env.API_URL}/report/result/`)
      const HeatmapOverlay = await require ('@/assets/leaflet-heatmap.js')
      this.heatMapLayer = new HeatmapOverlay(this.heatMapConfig)
      this.results = results

      this.map = new L.Map('map', {
        dragging: !L.Browser.mobile,
        maxZoom: 10,
        tap: !L.Browser.mobile,
        center: new L.LatLng(51.37328923, 10.21334121),
        zoom: 6,
        layers: [new L.TileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}{r}.png')]
      })

      this.createMap(results)
    } catch (e) {
      console.log(e)
    }
  },
  watch: {
    results: function() {}
  },
  watch: {
    zipCode: function(zipCode) {
      if (this.zipCodeRegex.test(zipCode)) {
        console.log(zipCode)

        this.$axios.$get(`${process.env.API_URL}/report/result/?new_format&zip_code=${zipCode}`).then(res => {
          this.results = res
          this.updateHeatmap(res)
        }).catch(e => {
          console.log(e)
        })
      }
    }
  },
  methods: {
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
    async updateHeatmap(response) {
      this.heatMapLayer.setData({data:[]})

      await this.normalizeResponse(response).forEach(async (item) => {
        try {
          this.heatMapStructure.data.push({
            lat: Number(item.latitude),
            lng: Number(item.longitude)
          })

          this.heatMapLayer.setData(this.heatMapStructure)
        } catch (e) {
          console.log(e)
        }
      })

      //this.map.removeLayer(this.heatMapLayer)
    },
    async createMap(response) {
      // eslint-disable-next-line no-undef
      if (document.getElementById('map')) {
        await this.normalizeResponse(response).forEach(async (item) => {
          try {
            this.heatMapStructure.data.push({
              lat: Number(item.latitude),
              lng: Number(item.longitude)
            })
            this.heatMapLayer.setData(this.heatMapStructure)
          } catch (e) {
            console.log(e);
          }
        })

        this.map.addLayer(this.heatMapLayer)
      }
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
