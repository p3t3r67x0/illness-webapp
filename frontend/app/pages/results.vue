<template>
  <v-container fill-height class="mx-auto">
    <v-layout class="layout" justify-center align-center color="blue lighten-2">
      <h1 class="blue--text headline">
        Übersicht der eingereichten Daten
      </h1>
      <br />
      <div class="map-container">
        <div id="map"></div>
      </div>
      <br />
      <br />
      <v-card
        class="mx-auto"
        outlined
      >
      <v-list two-line>
        <v-subheader>Symptome</v-subheader>
          <v-list-item v-for="(item, index) in normalizeResponse(results)" :key="index">
              <v-list-item-content>
                <v-list-item-title>{{ item.county }}</v-list-item-title>
                <div>
                  <v-chip v-for="symptom in formatSymptoms(item.symptoms)" class="ma-2">{{ symptom }}</v-chip>
                </div>
              </v-list-item-content>
          </v-list-item>
      </v-list>
      </v-card>
      <!--<div class="scroll-to-top">
        <a class="cursor-pointer rounded inline-block bg-blue-600 hover:bg-blue-800 text-white py-2 px-6" v-on:click.stop="scrollToTop">&#8593;</a>
      </div>-->
    </v-layout>
  </v-container>
</template>

<script>
  import { groupBy } from '../utils';
export default {
  data() {
    return {
      results: [],
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
      const results = await this.$axios.$get(`${process.env.API_URL}/report/result/`);
      this.results = results
      this.createMap(results)
    } catch (e) {
      console.log(e)
    }
  },
  watch: {
    results: function() {}
  },
  methods: {
    scrollToTop() {
      window.scrollTo({
        top: 0,
        left: 0,
        behavior: 'smooth'
      });
    },
    normalizeResponse(response) {
      const groupedResponse = groupBy(response, 'county')
      return  Object.keys(groupedResponse)
        .map(county => {
          console.log(groupedResponse[county])
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
    async createMap(response) {
      // eslint-disable-next-line no-undef
      if (document.getElementById('map')) {
        const L = this.$L;
        const HeatmapOverlay = await require('@/assets/leaflet-heatmap.js');
        const heatMapLayer = new HeatmapOverlay(this.heatMapConfig);

        await this.normalizeResponse(response).forEach(async (item) => {
          try {
            this.heatMapStructure.data.push({
              lat: Number(item.latitude),
              lng: Number(item.longitude)
            });
            heatMapLayer.setData(this.heatMapStructure)
          } catch (e) {
            console.log(e);
          }
        });

        const map = new L.Map('map', {
          dragging: !L.Browser.mobile,
          maxZoom: 10,
          tap: !L.Browser.mobile,
          center: new L.LatLng(51.37328923, 10.21334121),
          zoom: 6,
          layers: [new L.TileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}{r}.png'), heatMapLayer]
        });
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

  .layout {
    flex-direction: column;
  }

  .map-container {
    position: relative;
    display: block;
    width: 100%;
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
